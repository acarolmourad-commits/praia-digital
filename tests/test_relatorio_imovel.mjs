import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

// Behavior checks run the actual inline script with a minimal DOM substitute.
// These do not replace visual/browser verification.
const html = fs.readFileSync(fileURLToPath(new URL('../apps/relatorio-imovel/index.html', import.meta.url)), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const handlers = new Map();
function element(id) {
  return {id,value:'',textContent:'',hidden:false,focused:false,
    addEventListener(type,handler){handlers.set(`${id}:${type}`,handler);},
    focus(){this.focused=true;},classList:{toggle(){}}};
}
const controls = [...html.matchAll(/<(?:input|textarea|select)\b[^>]*\bid="([^"]+)"/g)].map(m=>element(m[1]));
controls.namedItem = name => controls.find(control=>control.id===name);
const nodes = Object.fromEntries([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>[m[1],element(m[1])]));
for(const control of controls) nodes[control.id]=control;
const outputs = [...html.matchAll(/<[^>]+\bdata-field="([^"]+)"([^>]*)>/g)].map(m=>{
  const node=element();node.dataset={field:m[1]};
  const empty=m[2].match(/data-empty="([^"]+)"/);if(empty)node.dataset.empty=empty[1];
  return node;
});
nodes['report-form'].elements=controls;
nodes['report-form'].reset=()=>controls.forEach(control=>control.value='');
let allowConfirm=true,printed=0;
const context={document:{getElementById:id=>nodes[id],querySelectorAll:()=>outputs},window:{confirm:()=>allowConfirm,print:()=>printed++,addEventListener:(type,handler)=>handlers.set(`window:${type}`,handler)}};
vm.runInNewContext(script,context);
const output=id=>outputs.find(o=>o.dataset.field===id).textContent;
const click=id=>handlers.get(`${id}:click`)();
const input=(id,value)=>{nodes[id].value=value;handlers.get('report-form:input')();};
assert.equal(output('partner'),'Nome do parceiro');
assert.equal(output('price'),'A confirmar');
assert.equal(nodes['example-notice'].hidden,true);
input('partner','<img src=x onerror=alert(1)>');
assert.equal(output('partner'),'<img src=x onerror=alert(1)>');
assert.ok(outputs.every(node=>!Object.hasOwn(node,'innerHTML')));
input('referenceDate','2026-11-12');assert.equal(output('referenceDate'),'12/11/2026');
allowConfirm=false;click('load-example');assert.equal(output('partner'),'<img src=x onerror=alert(1)>');
allowConfirm=true;click('load-example');
assert.equal(nodes['example-notice'].hidden,false);
assert.match(output('sources'),/fictícia/);
assert.equal(output('purpose'),'Locação mensal');
input('objective','Objetivo editado');assert.equal(nodes['example-notice'].hidden,false);
nodes.objective.value='Texto atualizado imediatamente antes de imprimir';
handlers.get('window:beforeprint')();
assert.equal(output('objective'),'Texto atualizado imediatamente antes de imprimir');
input('objective','Objetivo editado');
click('print-report');assert.equal(printed,1);
allowConfirm=false;click('clear-report');assert.equal(output('objective'),'Objetivo editado');
allowConfirm=true;click('clear-report');
assert.ok(controls.every(control=>control.value===''));
assert.equal(output('purpose'),'A confirmar');
assert.equal(nodes['example-notice'].hidden,true);
assert.equal(nodes.partner.focused,true);
assert.doesNotMatch(script,/fetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|innerHTML\s*=/);
// Verify discovery and accessibility wiring in the generated production page.
assert.doesNotMatch(html,/<meta\b[^>]+name=["']robots["'][^>]+noindex/i);
assert.equal((html.match(/rel="canonical"/g)||[]).length,1);
assert.match(html,/rel="canonical" href="https:\/\/praia\.digital\/apps\/relatorio-imovel\/"/);
assert.equal((html.match(/<h1\b/g)||[]).length,1);
assert.match(html,/name="description" content="[^"]+"/);
for(const id of ['main-content','report']) assert.match(html,new RegExp(`href="#${id}"`));
assert.ok(outputs.every(node=>controls.some(control=>control.id===node.dataset.field)));
assert.equal(controls.length,17);
assert.equal(outputs.length,17);

// Pages replaces the app header and injects a stylesheet after our inline CSS.
// Exercise that real transformation without changing any repository file.
const root = fileURLToPath(new URL('../', import.meta.url));
const transformed = spawnSync('python3', ['-c', String.raw`
import importlib.util, json, sys
from pathlib import Path
from html.parser import HTMLParser
sys.dont_write_bytecode = True
root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('pd_navigation', root / 'scripts/build-navigation.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = (root / 'apps/relatorio-imovel/index.html').read_text()
result, included = module.transform(source, (root / 'partials/header.html').read_text())
assert included
class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.direct_body_classes = []
        self.report_ancestors = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        if self.stack and self.stack[-1][0] == 'body':
            self.direct_body_classes.extend(classes)
        if attrs.get('id') == 'report':
            self.report_ancestors = [item[1] for item in self.stack]
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append((tag, classes))
    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break
parser = Structure()
parser.feed(result)
print(json.dumps({'html': result, 'directBodyClasses': parser.direct_body_classes,
                 'reportAncestors': parser.report_ancestors}))
`, root], { encoding: 'utf8' });
assert.equal(transformed.status, 0, transformed.stderr);
const deployed = JSON.parse(transformed.stdout);
assert.ok(deployed.directBodyClasses.includes('pd-site-header'));
assert.ok(deployed.directBodyClasses.includes('pd-preserved-intro'));
assert.ok(Array.isArray(deployed.reportAncestors));
assert.ok(deployed.reportAncestors.every(classes =>
  !classes.includes('pd-site-header') && !classes.includes('pd-preserved-intro')));

const printStart = deployed.html.indexOf('@media print{');
assert.ok(printStart >= 0);
const printCss = deployed.html.slice(printStart, deployed.html.indexOf('</style>', printStart));
assert.match(printCss,
  /body\s*>\s*\.pd-site-header\s*,\s*body\s*>\s*\.pd-preserved-intro\s*\{\s*display\s*:\s*none\s*!important\s*\}/);
// The body type selector raises specificity above the shared .pd-site-header
// rule, even though the shared stylesheet is loaded after the local styles.
const navigationCss = fs.readFileSync(new URL('../assets/css/pd-navigation.css', import.meta.url), 'utf8');
assert.match(navigationCss, /\.pd-site-header\s*\{[^}]*display\s*:\s*block\s*!important/);
assert.match(printCss, /\.layout\s*\{[^}]*display\s*:\s*block/);
const reportHtml = text => text.match(/<article class="report"[\s\S]*?<\/article>/)[0];
assert.equal(reportHtml(deployed.html), reportHtml(html));
assert.equal(deployed.html.match(/<script>([\s\S]*?)<\/script>/)[1], script);
assert.ok(deployed.html.indexOf('/assets/css/pd-navigation.css') > deployed.html.indexOf('@media print{'));
console.log('Behavior, metadata, accessibility wiring and transformed print regression passed; browser/layout QA remains separate.');
