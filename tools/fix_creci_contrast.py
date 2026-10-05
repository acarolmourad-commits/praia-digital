import re

CSS = """<style>
body{font-family:'Segoe UI',Arial,Helvetica,sans-serif;background:#F4EBD0;color:#023047;margin:0;padding:0;line-height:1.6}
.container{max-width:900px;margin:0 auto;padding:20px;background:#FFFFFF;border-radius:12px;margin-top:20px;margin-bottom:20px;box-shadow:0 2px 12px rgba(2,48,71,.08)}
a{color:#0077B6;text-decoration:underline}
a:hover{color:#00B4D8}
.nav{margin-bottom:20px}
.nav a{margin-right:10px}
.card{background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px;padding:16px;margin:12px 0;color:#023047}
.badge{display:inline-block;background:#0077B6;color:#fff;padding:4px 8px;border-radius:999px;font-size:12px;margin:4px 6px 0 0}
.cta{background:#0077B6;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;display:inline-block;margin:16px 0}
.cta:hover{background:#023047;color:#fff}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px;background:#FFFFFF;color:#023047}
th{background:#0077B6;color:#FFFFFF;text-align:left;padding:10px}
td{border:1px solid #d0d7de;padding:9px;color:#023047}
tr:nth-child(even){background:#f6f8fa}
.bar-wrap{background:#e5e7eb;border-radius:6px;overflow:hidden;margin:4px 0 14px}
.bar{background:#0077B6;color:#FFFFFF;padding:6px 10px;font-size:13px;white-space:nowrap}
.bar.green{background:#2d9e5a}.bar.orange{background:#F97316}
.formula{background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:12px 16px;font-family:Consolas,monospace;font-size:15px;margin:10px 0;display:inline-block;color:#023047}
.kbd{background:#eaeef2;border-radius:5px;padding:2px 8px;font-family:Consolas,monospace;font-size:13px;border:1px solid #c8d0d8;color:#023047}
h2{margin-top:34px;color:#023047}
h3{color:#0077B6}
.note{border-left:4px solid #F59E0B;background:#FFF8E6;padding:10px 14px;margin:14px 0;border-radius:0 8px 8px 0;color:#023047}
strong{color:#023047}
</style>"""

p = 'blog/simulados-gratis-creci-2026.html'
t = open(p, encoding='utf-8').read()
start = t.index('<style>')
end = t.index('</style>') + len('</style>')
t = t[:start] + CSS + t[end:]
open(p, 'w', encoding='utf-8').write(t)
print('ok', len(t))
