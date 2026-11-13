import {readFile,writeFile} from 'node:fs/promises';
const files={'/':['index.html','text/html; charset=utf-8'],'/app.js':['app.js','application/javascript; charset=utf-8'],'/style.css':['style.css','text/css; charset=utf-8'],'/domain.mjs':['domain.mjs','application/javascript; charset=utf-8']};
const assets={};for(const [url,[file,type]]of Object.entries(files))assets[url]={type,body:await readFile(new URL(file,import.meta.url),'utf8')};
assets['/robots.txt']={type:'text/plain',body:'User-agent: *\nDisallow: /\n'};
await writeFile(new URL('assets.mjs',import.meta.url),'export const assets='+JSON.stringify(assets)+';\n');
console.log('Assets prepared.');
