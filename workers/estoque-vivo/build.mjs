import {readFile,writeFile} from 'node:fs/promises';
const files={'/':['index.html','text/html; charset=utf-8'],'/app.js':['app.js','application/javascript; charset=utf-8'],'/style.css':['style.css','text/css; charset=utf-8'],'/domain.mjs':['domain.mjs','application/javascript; charset=utf-8']};
files['/sw.js']=['sw.js','application/javascript; charset=utf-8'];files['/manifest.webmanifest']=['manifest.webmanifest','application/manifest+json'];
files['/orders-ui.js']=['orders-ui.js','application/javascript; charset=utf-8'];files['/integracao.html']=['integracao.html','text/html; charset=utf-8'];
files['/apresentacao.html']=['apresentacao.html','text/html; charset=utf-8'];files['/apresentacao.css']=['apresentacao.css','text/css; charset=utf-8'];
files['/production-ui.js']=['production-ui.js','application/javascript; charset=utf-8'];
files['/piloto.html']=['piloto.html','text/html; charset=utf-8'];files['/piloto.css']=['piloto.css','text/css; charset=utf-8'];
const assets={};for(const [url,[file,type]]of Object.entries(files))assets[url]={type,body:await readFile(new URL(file,import.meta.url),'utf8')};
for(const size of [180,192,512])assets[`/icon-${size}.png`]={type:'image/png',encoding:'base64',body:(await readFile(new URL(`icon-${size}.png`,import.meta.url))).toString('base64')};
assets['/robots.txt']={type:'text/plain',body:'User-agent: *\nDisallow: /\n'};
await writeFile(new URL('assets.mjs',import.meta.url),'export const assets='+JSON.stringify(assets)+';\n');
console.log('Assets prepared.');

import {build} from 'esbuild';
await build({entryPoints:[new URL('worker.mjs',import.meta.url).pathname],bundle:true,format:'esm',platform:'neutral',external:['cloudflare:workers'],outfile:new URL('dist/worker.mjs',import.meta.url).pathname});
