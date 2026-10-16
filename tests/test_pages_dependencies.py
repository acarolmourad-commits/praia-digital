import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SPEC=importlib.util.spec_from_file_location("dependency_audit",Path(__file__).resolve().parents[1]/"scripts/audit_pages_dependencies.py")
AUDIT=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(AUDIT)

class DependencyAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name); self.source=self.root/"checkout"; self.source.mkdir()
        self.write("index.html","<h1>Synthetic page</h1>")
    def write(self,name,text):
        path=self.source/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding="utf-8")
    def run_audit(self,files=None,entries=(),**kwargs):
        return AUDIT.audit(self.source,{"version":1,"reviewed":False,"files":files if files is not None else ["index.html"]},entries,**kwargs)
    def codes(self,r): return {a["code"] for a in r["alerts"]}
    def targets(self,r): return {d["to"] for d in r["dependencies"]}
    def test_never_approves(self):
        for reviewed in (True,False):
            report=AUDIT.audit(self.source,{"version":1,"reviewed":reviewed,"files":["index.html"]})
            self.assertIs(report["publication_approved"],False)
    def test_empty_manifest_is_partial(self):
        r=self.run_audit([],entries=["index.html"])
        self.assertTrue({"manifest_empty","manifest_not_reviewed","not_in_manifest"}<=self.codes(r))
    def test_html_css_closure(self):
        self.write("index.html",'<link href="assets/site.css"><a href="section/">Link</a>')
        self.write("assets/site.css",'@import "more.css"; body {background:url("image.png")}')
        self.write("assets/more.css",'body{}'); self.write("assets/image.png","SYNTHETIC")
        self.write("section/index.html",'<img src="../assets/image.png">')
        r=self.run_audit(); self.assertEqual(set(r['paths']),{'index.html','assets/site.css','assets/more.css','assets/image.png','section/index.html'})
    def test_js_literals(self):
        self.write("index.html",'<script src="js/main.js"></script>')
        self.write("js/main.js",'import "./module.js"; fetch("/assets/data.json?token=SYNTHETIC_SECRET");')
        self.write("js/module.js",'console.log("SYNTHETIC_BODY");'); self.write("assets/data.json",'{}')
        r=self.run_audit(); self.assertTrue({'js/module.js','assets/data.json'}<=self.targets(r)); self.assertIn('javascript_requires_manual_review',self.codes(r))
        self.assertNotIn('SYNTHETIC_SECRET',json.dumps(r)); self.assertNotIn('SYNTHETIC_BODY',json.dumps(r))
    def test_blocked_not_read(self):
        self.write("index.html",'<a href="docs/sales/example.html">Internal</a>')
        self.write("docs/sales/example.html","SYNTHETIC_PRIVATE_BODY")
        r=self.run_audit(); self.assertNotIn('docs/sales/example.html',r['paths']); self.assertIn('blocked_path',self.codes(r)); self.assertNotIn('SYNTHETIC_PRIVATE_BODY',json.dumps(r))
    def test_operational_page_blocked(self):
        self.write('index.html','<a href="ACOES-HOJE.HTML">internal</a>'); self.write('ACOES-HOJE.HTML','SYNTHETIC')
        self.assertIn('blocked_path',self.codes(self.run_audit()))
    def test_missing(self):
        self.write('index.html','<img src="absent.png">'); self.assertIn('missing_file',self.codes(self.run_audit()))
    def test_query_fragment_removed(self):
        self.assertEqual(AUDIT.resolve_reference('index.html','assets/a.css?secret=SYNTHETIC#fragment'),('assets/a.css',None))
    def test_contacts_and_external_redacted(self):
        self.write('index.html','<a href="mailto:synthetic@example.invalid">Email</a><a href="https://outside.invalid/x?token=SYNTHETIC">external</a>')
        r=self.run_audit(); s=json.dumps(r); self.assertNotIn('example.invalid',s); self.assertNotIn('outside.invalid',s); self.assertNotIn('SYNTHETIC',s)
    def test_own_origin(self):
        self.assertEqual(AUDIT.resolve_reference('index.html','https://praia.digital/section/?token=SYNTHETIC'),('section/index.html',None))
    def test_credentials_redacted(self):
        self.assertEqual(AUDIT.resolve_reference('index.html','https://synthetic:secret@praia.digital/a.html'),(None,'unsafe_reference'))
    def test_encoded_traversal(self):
        for ref in ('%2e%2e/secret.html','%252e%252e/secret.html','..\\secret.html','assets/%00secret.html'):
            with self.subTest(ref=ref): self.assertEqual(AUDIT.resolve_reference('index.html',ref),(None,'unsafe_reference'))
    def test_unsafe_contact_path_redacted(self):
        self.write('index.html','<a href="synthetic@example.invalid.html">private name</a>')
        r=self.run_audit(); self.assertNotIn('example.invalid',json.dumps(r)); self.assertIn('unsafe_reference',self.codes(r))
    def test_fragment_only(self): self.assertEqual(AUDIT.resolve_reference('index.html','#anchor'),(None,None))
    def test_symlink_file(self):
        (self.source/'alias.html').symlink_to(self.source/'index.html'); r=self.run_audit(['alias.html']); self.assertEqual(r['paths'],[]); self.assertIn('symlink_not_read',self.codes(r))
    def test_symlink_directory(self):
        (self.source/'alias').symlink_to(self.source,target_is_directory=True); self.assertIn('symlink_not_read',self.codes(self.run_audit(['alias/index.html'])))
    def test_symlink_source(self):
        alias=self.root/'alias'; alias.symlink_to(self.source,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'unsafe_source'): AUDIT.audit(alias,{"version":1,"reviewed":False,"files":[]})
    def test_invalid_manifest(self):
        for value in ({'version':True,'reviewed':False,'files':[]},{'version':1,'reviewed':'false','files':[]},{'version':1,'reviewed':False,'files':['../secret.html']},{'version':1,'reviewed':False,'files':['x@example.invalid.html']}):
            with self.subTest(value=value):
                with self.assertRaises(ValueError): AUDIT.audit(self.source,value)
    def test_invalid_entry(self):
        with self.assertRaises(ValueError): self.run_audit(entries=['../secret.html'])
    def test_duplicate(self): self.assertIn('duplicate_manifest_paths',self.codes(self.run_audit(['index.html','index.html'])))
    def test_json_no_body(self):
        self.write('site.webmanifest',json.dumps({'start_url':'/index.html','icons':[{'src':'/icon.png'}],'private':'SYNTHETIC_PRIVATE'})); self.write('icon.png','SYNTHETIC')
        r=self.run_audit(['site.webmanifest']); self.assertIn('icon.png',self.targets(r)); self.assertNotIn('SYNTHETIC_PRIVATE',json.dumps(r))
    def test_xml(self):
        self.write('sitemap.xml','<urlset><url><loc>https://praia.digital/index.html?secret=SYNTHETIC</loc></url></urlset>'); r=self.run_audit(['sitemap.xml']); self.assertIn('index.html',self.targets(r)); self.assertNotIn('SYNTHETIC',json.dumps(r))
    def test_xml_entities(self):
        self.write('site.xml','<!DOCTYPE x [<!ENTITY s SYSTEM "file:///tmp/private">]><x>&s;</x>'); self.assertIn('xml_entities_not_parsed',self.codes(self.run_audit(['site.xml'])))
    def test_invalid_json(self):
        self.write('bad.json','{SYNTHETIC_PRIVATE'); r=self.run_audit(['bad.json']); self.assertIn('file_not_parsed',self.codes(r)); self.assertNotIn('SYNTHETIC_PRIVATE',json.dumps(r))
    def test_size_limit(self):
        self.write('index.html','x'*(AUDIT.MAX_BYTES+1)); self.assertIn('file_too_large',self.codes(self.run_audit()))
    def test_file_limit(self):
        self.write('index.html','<a href="next.html">next</a>'); self.write('next.html','SYNTHETIC'); self.assertIn('file_limit_reached',self.codes(self.run_audit(max_files=1)))
    def test_base_alert(self):
        self.write('index.html','<base href="/section/">'); self.assertIn('base_url_requires_manual_review',self.codes(self.run_audit()))
    def test_readonly_and_deterministic(self):
        before={p.relative_to(self.source):p.read_bytes() for p in self.source.rglob('*') if p.is_file()}
        self.assertEqual(self.run_audit(),self.run_audit())
        after={p.relative_to(self.source):p.read_bytes() for p in self.source.rglob('*') if p.is_file()}; self.assertEqual(before,after)
    def test_cli_invalid_input_no_traceback(self):
        path=self.root/'manifest.json'; path.write_text('{SYNTHETIC_PRIVATE')
        r=subprocess.run([sys.executable,str(Path(AUDIT.__file__)), '--source',str(self.source),'--manifest',str(path)],capture_output=True,text=True)
        self.assertEqual(r.returncode,2); self.assertEqual(r.stderr,''); self.assertNotIn('SYNTHETIC_PRIVATE',r.stdout); self.assertNotIn(str(self.root),r.stdout)

if __name__=='__main__': unittest.main()
