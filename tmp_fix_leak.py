from pathlib import Path
import re

base = Path('assets')
issues = {
    'analise-retorno-aluguel-temporada-ia.html': [
        (
            '</html><div id="result-analise-retorno-aluguel-temporada-ia" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-analise-retorno-aluguel-temporada-ia");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script></body>',
            '<div id="result-analise-retorno-aluguel-temporada-ia" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-analise-retorno-aluguel-temporada-ia");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script>'
        )
    ],
    'predicao-vendidos-litoral.html': [
        (
            '</html><div id="result-predicao-vendidos-litoral" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-predicao-vendidos-litoral");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script></body>',
            '<div id="result-predicao-vendidos-litoral" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-predicao-vendidos-litoral");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script>'
        )
    ],
    'roi-ia-imobiliaria.html': [
        (
            '</html><div id="result-roi-ia-imobiliaria" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-roi-ia-imobiliaria");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script></body>',
            '<div id="result-roi-ia-imobiliaria" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-roi-ia-imobiliaria");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script>'
        )
    ],
    'servico-assistente-virtual-compradores-litoral.html': [
        (
            '</html><div id="result-servico-assistente-virtual-compradores-litoral" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-servico-assistente-virtual-compradores-litoral");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script></body>',
            '<div id="result-servico-assistente-virtual-compradores-litoral" class="result">Resultado</div><script>async function run(){const out=document.getElementById("result-servico-assistente-virtual-compradores-litoral");out.textContent="Processando...";const payload={};document.querySelectorAll("#integrated-form [name]").forEach(el=>{const n=el.getAttribute("name");payload[n]=isNaN(Number(el.value))?el.value:Number(el.value);});const e=await fetch("http://127.0.0.1:8000/avaliar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await e.json();out.textContent=JSON.stringify(d,null,2)}document.getElementById("integrated-form").addEventListener("submit",function(e){e.preventDefault();run()});document.getElementById("b-run")?.addEventListener("click",run);</script>'
        )
    ]
}
for fname, pairs in issues.items():
    p = base / fname
    text = p.read_text(encoding='utf-8', errors='ignore')
    original = text
    for old, new in pairs:
        text = text.replace(old, new, 1)
    if fname == 'analise-retorno-aluguel-temporada-ia.html':
        text = text.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots"', '<meta name="robots"', 1)
    if fname == 'predicao-vendidos-litoral.html':
        text = text.replace('</head><body><header', '</head>\n<body><header', 1)
    if fname == 'roi-ia-imobiliaria.html':
        text = text.replace('<footer>\n</html>\n<div', '<footer>\n</div>\n<div', 1)
        text = text.replace('</html>\n</body>', '</div>\n</body>', 1)
        text = text.replace('<body>\n<header', '<body>\n<header', 1)
    if text != original:
        p.write_text(text, encoding='utf-8')
        print('patched', fname)
    else:
        print('nochange', fname)
