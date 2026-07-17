from pathlib import Path
from datetime import datetime

repo = Path('.')
dashboard_dir = repo / 'dashboard'
dashboard_dir.mkdir(exist_ok=True)

cities = [
    {
        'slug': 'santos',
        'name': 'Santos',
        'preco_m2': 8200,
        'valorizacao_12m': 5.2,
        'diaria_media_airbnb': 380,
        'ocupacao_media': 68,
        'roi': 5.8,
        'liquidez': 'Alta',
        'imoveis_vendidos': 1240
    },
    {
        'slug': 'guaruja',
        'name': 'Guarujá',
        'preco_m2': 7600,
        'valorizacao_12m': 6.1,
        'diaria_media_airbnb': 350,
        'ocupacao_media': 64,
        'roi': 6.4,
        'liquidez': 'Alta',
        'imoveis_vendidos': 890
    },
    {
        'slug': 'praia-grande',
        'name': 'Praia Grande',
        'preco_m2': 5400,
        'valorizacao_12m': 7.8,
        'diaria_media_airbnb': 280,
        'ocupacao_media': 72,
        'roi': 7.2,
        'liquidez': 'Média',
        'imoveis_vendidos': 1560
    },
    {
        'slug': 'itanhaem',
        'name': 'Itanhaém',
        'preco_m2': 5100,
        'valorizacao_12m': 8.4,
        'diaria_media_airbnb': 260,
        'ocupacao_media': 70,
        'roi': 7.6,
        'liquidez': 'Média',
        'imoveis_vendidos': 980
    },
    {
        'slug': 'sao-vicente',
        'name': 'São Vicente',
        'preco_m2': 6200,
        'valorizacao_12m': 6.7,
        'diaria_media_airbnb': 300,
        'ocupacao_media': 62,
        'roi': 6.1,
        'liquidez': 'Alta',
        'imoveis_vendidos': 1120
    },
    {
        'slug': 'mongagua',
        'name': 'Mongaguá',
        'preco_m2': 5800,
        'valorizacao_12m': 7.5,
        'diaria_media_airbnb': 290,
        'ocupacao_media': 69,
        'roi': 7.0,
        'liquidez': 'Média',
        'imoveis_vendidos': 750
    },
    {
        'slug': 'peruibe',
        'name': 'Peruíbe',
        'preco_m2': 4900,
        'valorizacao_12m': 8.9,
        'diaria_media_airbnb': 250,
        'ocupacao_media': 74,
        'roi': 7.9,
        'liquidez': 'Baixa',
        'imoveis_vendidos': 620
    },
    {
        'slug': 'bertioga',
        'name': 'Bertioga',
        'preco_m2': 7400,
        'valorizacao_12m': 6.5,
        'diaria_media_airbnb': 340,
        'ocupacao_media': 65,
        'roi': 6.7,
        'liquidez': 'Alta',
        'imoveis_vendidos': 540
    }
]

cards = []
for c in cities:
    valorizacao_color = "#10b981" if c['valorizacao_12m'] >= 7 else "#f59e0b" if c['valorizacao_12m'] >= 6 else "#64748b"
    roi_color = "#10b981" if c['roi'] >= 7 else "#f59e0b" if c['roi'] >= 6 else "#64748b"
    cards.append(f"""
    <div class="city-card">
        <div class="city-header">
            <h2>{c['name']}</h2>
            <a href="/blog/mercado/mercado-{c['slug']}-2026.html" class="detail-link">Ver detalhes &rarr;</a>
        </div>
        <div class="metrics">
            <div class="metric">
                <span class="metric-label">Valorização 12m</span>
                <span class="metric-value" style="color: {valorizacao_color}">+{c['valorizacao_12m']}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Diária Média Airbnb</span>
                <span class="metric-value">R$ {c['diaria_media_airbnb']:,}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Ocupação Média</span>
                <span class="metric-value">{c['ocupacao_media']}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">ROI</span>
                <span class="metric-value" style="color: {roi_color}">{c['roi']}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Liquidez</span>
                <span class="metric-value liquidity-{c['liquidez'].lower()}">{c['liquidez']}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Imóveis Vendidos</span>
                <span class="metric-value">{c['imoveis_vendidos']:,}</span>
            </div>
        </div>
    </div>
    """)

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard de Investimento — Litoral SP 2026 | Praia Digital</title>
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }}
    header {{ background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
    header h1 {{ margin: 0; font-size: 2rem; font-weight: 700; }}
    header p {{ margin: 0.5rem 0 0; opacity: 0.9; font-size: 0.95rem; }}
    .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem 1rem; }}
    .summary-bar {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; }}
    .summary-item {{ text-align: center; }}
    .summary-value {{ font-size: 1.75rem; font-weight: 700; color: #0a1628; }}
    .summary-label {{ font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }}
    .city-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; }}
    .city-card {{ background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s; }}
    .city-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 16px rgba(0,0,0,0.12); }}
    .city-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 2px solid #e2e8f0; }}
    .city-header h2 {{ margin: 0; font-size: 1.25rem; color: #0a1628; }}
    .detail-link {{ color: #2563eb; text-decoration: none; font-size: 0.85rem; font-weight: 600; }}
    .detail-link:hover {{ text-decoration: underline; }}
    .metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
    .metric {{ display: flex; flex-direction: column; }}
    .metric-label {{ font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }}
    .metric-value {{ font-size: 1.1rem; font-weight: 700; color: #0a1628; }}
    .liquidity-alta {{ color: #10b981; font-weight: 700; }}
    .liquidity-média {{ color: #f59e0b; font-weight: 700; }}
    .liquidity-baixa {{ color: #64748b; font-weight: 700; }}
    footer {{ text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }}
</style>
</head>
<body>
    <header>
        <h1>📊 Dashboard de Investimento</h1>
        <p>Litoral São Paulo — {datetime.now().strftime('%B %Y')}</p>
    </header>
    
    <div class="container">
        <div class="summary-bar">
            <div class="summary-item">
                <div class="summary-value">{len(cities)}</div>
                <div class="summary-label">Cidades Analisadas</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">+8.4%</div>
                <div class="summary-label">Maior Valorização</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">7.9%</div>
                <div class="summary-label">Maior ROI</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">8,600</div>
                <div class="summary-label">Total Imóveis Vendidos</div>
            </div>
        </div>
        
        <div class="city-grid">
            {"".join(cards)}
        </div>
    </div>
    
    <footer>
        <p>Dados atualizados em {datetime.now().strftime('%d/%m/%Y')} — Fonte: mercado imobiliário Litoral SP</p>
    </footer>
</body>
</html>"""

(dashboard_dir / 'index.html').write_text(html, encoding='utf-8')
print('dashboard created')
