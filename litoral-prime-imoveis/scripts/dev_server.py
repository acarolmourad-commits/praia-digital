"""
Litoral Prime — servidor local para desenvolvimento e captura de leads.
Rode: uv run python scripts/dev_server.py
Acesse: http://localhost:8000
Obs.: para produção, use hosting com backend ou forms externos.
"""
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import csv, datetime, json, base64

BASE = Path(__file__).resolve().parent.parent
LEADS_FILE = BASE / "outreach" / "leads-site.csv"
METRICAS_FILE = BASE / "outreach" / "metricas.csv"


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/scripts/captura_lead.py"):
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            lead = {k: (v[0] if v else "").strip() for k, v in params.items()}
            lead.setdefault("data", datetime.date.today().isoformat())
            lead.setdefault("nome", "")
            lead.setdefault("email", "")
            lead.setdefault("telefone", "")
            lead.setdefault("interesse", "")
            lead.setdefault("mensagem", "")
            exists = LEADS_FILE.exists()
            with LEADS_FILE.open("a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["data", "nome", "email", "telefone", "interesse", "mensagem"])
                if not exists:
                    writer.writeheader()
                writer.writerow(lead)
            self.send_response(204)
            self.end_headers()
            return

        if self.path.startswith("/scripts/save_metricas.py"):
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            payload_b64 = (params.get("payload", [""])[0] or "").strip()
            if not payload_b64:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"{}")
                return
            try:
                rows = json.loads(base64.b64decode(payload_b64).decode("utf-8"))
                if not rows:
                    raise ValueError("vazio")
                fieldnames = list(rows[0].keys())
                with METRICAS_FILE.open("w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for r in rows:
                        writer.writerow({k: r.get(k, "") for k in fieldnames})
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "saved": len(rows)}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode("utf-8"))
            return

        return super().do_GET()


if __name__ == "__main__":
    port = 8000
    print(f"Servidor local em http://localhost:{port}")
    HTTPServer(("", port), Handler).serve_forever()
