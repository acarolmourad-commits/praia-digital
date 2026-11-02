// Filename-scoped inventory of the actual baseline; avoids counting footer mentions as city content.
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
const base=process.argv[2]||'04e83b23dff4ef271de5f4c11b0899ebad6a1c63';
const git=(...args)=>cp.execFileSync('git',args,{cwd:root,encoding:'utf8',maxBuffer:20*1024*1024});
const files=git('ls-tree','-r','--name-only',base).trim().split('\n');
const cities=JSON.parse(fs.readFileSync(path.join(root,'data/city-guides.json'),'utf8')).cities;
const cachedPath=path.join(root,'.audit/city-guides/inventory.json');
const cached=fs.existsSync(cachedPath)?JSON.parse(fs.readFileSync(cachedPath,'utf8')):null;
const cache=new Map(cached?.base===base?cached.cities.flatMap(c=>c.entries).map(e=>[e.path,e]):[]);
const meta=file=>{if(cache.has(file))return cache.get(file);const text=git('show',`${base}:${file}`);const entry={path:file,title:(text.match(/<title[^>]*>([\s\S]*?)<\/title>/i)||[])[1]||'',canonical:(text.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']+)/i)||[])[1]||'',sha256:crypto.createHash('sha256').update(text).digest('hex')};cache.set(file,entry);return entry};
const sitemap=git('show',base+':sitemap.xml');
const report={base,scope:'16 municipalities in the three coastal sectors; Cubatão included regionally, inland Vale do Ribeira excluded',method:'Paths containing municipal slug (not footer/body mentions); exact bytes and canonical recorded for potential duplicates. Inventory is not factual endorsement.',cities:[]};
for(const c of cities){
 const matches=files.filter(f=>f.endsWith('.html')&&new RegExp(`(^|[/-])${c.slug}([/.-]|$)`).test(f)&&(/^(cidades|blog|bairros|cidades-expansao)\//.test(f)||!f.includes('/')));
 const entries=matches.map(meta);
 report.cities.push({name:c.name,slug:c.slug,region:c.region,before:{guide:files.includes(`cidades/${c.slug}.html`),neighborhoodHub:files.includes(`bairros/${c.slug}/index.html`),blogCount:entries.filter(e=>e.path.startsWith('blog/')).length,inSitemap:sitemap.includes(`https://praia.digital/cidades/${c.slug}.html`)},after:{guide:`/cidades/${c.slug}.html`,neighborhoodHub:files.includes(`bairros/${c.slug}/index.html`)?`/bairros/${c.slug}/index.html`:null},entries});
}
const entries=[...new Map(report.cities.flatMap(c=>c.entries).map(e=>[e.path,e])).values()];
report.uniqueCandidateFiles=entries.length;
report.note='Counts are filename candidates, not verified articles: Praia Grande can also name a beach in Ubatuba; multi-city articles may appear in multiple city lists. Duplicate analysis deduplicates paths first.';
report.potentialDuplicateCanonicals=Object.entries(Object.groupBy(entries,e=>e.canonical)).filter(([k,v])=>k&&v.length>1).map(([canonical,v])=>({canonical,paths:v.map(e=>e.path)}));
report.exactDuplicateContents=Object.values(Object.groupBy(entries,e=>e.sha256)).filter(v=>v.length>1).map(v=>v.map(e=>e.path));
report.retainedAlternativeRoutes=entries.filter(e=>!e.path.startsWith('blog/')&&!e.path.startsWith('bairros/')&&!/^cidades\/[^/]+\.html$/.test(e.path));
fs.mkdirSync(path.join(root,'.audit/city-guides'),{recursive:true});
fs.writeFileSync(path.join(root,'.audit/city-guides/inventory.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report.cities.map(({name,before,after})=>({name,...before,after:after.guide})),null,2));
