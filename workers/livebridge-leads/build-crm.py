"""Regenerate the Worker UI module from editable HTML/CSS/JS sources."""
from pathlib import Path
import json
root = Path(__file__).resolve().parent
(root / 'crm-ui.mjs').write_text('\n'.join('export const '+name+' = '+json.dumps((root/file).read_text(),ensure_ascii=False)+';' for name,file in [('HTML','crm.html'),('CSS','crm.css'),('JS','crm.js')]))
