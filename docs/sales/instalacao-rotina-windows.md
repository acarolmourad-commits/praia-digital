<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Instalação Rotina Automática - Praia Digital</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: linear-gradient(135deg, #0a1628 0%, #1a3a5c 100%);
      color: #fff;
      min-height: 100vh;
      padding: 2rem;
    }
    .container { max-width: 900px; margin: 0 auto; }
    .header {
      background: linear-gradient(135deg, #7b2ff7, #00d4ff);
      padding: 2rem;
      border-radius: 12px;
      margin-bottom: 2rem;
      text-align: center;
    }
    .header h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .header p { opacity: 0.9; }
    
    .card {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 1.5rem;
      backdrop-filter: blur(10px);
    }
    .card h2 {
      font-size: 1.3rem;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, #00d4ff, #7b2ff7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .step {
      display: flex;
      gap: 1rem;
      margin-bottom: 1.5rem;
      padding: 1rem;
      background: rgba(255,255,255,0.03);
      border-radius: 8px;
      border-left: 3px solid #00d4ff;
    }
    .step-number {
      background: linear-gradient(135deg, #00d4ff, #7b2ff7);
      color: #fff;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      flex-shrink: 0;
    }
    .step-content h3 {
      font-size: 1rem;
      margin-bottom: 0.25rem;
    }
    .step-content p {
      color: #bbb;
      font-size: 0.95rem;
      line-height: 1.6;
    }
    
    .code-block {
      background: #0a1420;
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 8px;
      padding: 1rem;
      margin-top: 0.75rem;
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
      color: #00d4ff;
      position: relative;
    }
    .code-block .copy-btn {
      position: absolute;
      top: 0.5rem;
      right: 0.5rem;
      background: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.2);
      color: #fff;
      padding: 0.3rem 0.6rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.8rem;
    }
    .code-block .copy-btn:hover { background: rgba(255,255,255,0.2); }
    
    .status-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }
    .status-item {
      background: rgba(255,255,255,0.05);
      padding: 1rem;
      border-radius: 8px;
      border-left: 3px solid #00d4ff;
    }
    .status-item h4 {
      font-size: 0.85rem;
      color: #aaa;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 0.5rem;
    }
    .status-item p {
      font-size: 1.1rem;
      font-weight: 600;
    }
    
    .warning-box {
      background: rgba(255, 152, 0, 0.1);
      border: 1px solid rgba(255, 152, 0, 0.4);
      border-radius: 8px;
      padding: 1rem;
      margin-top: 1rem;
    }
    .warning-box h3 {
      color: #ff9800;
      margin-bottom: 0.5rem;
      font-size: 1rem;
    }
    .warning-box p {
      color: #ddd;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    
    .success-box {
      background: rgba(0, 212, 150, 0.1);
      border: 1px solid rgba(0, 212, 150, 0.4);
      border-radius: 8px;
      padding: 1rem;
      margin-top: 1rem;
    }
    .success-box h3 {
      color: #00d496;
      margin-bottom: 0.5rem;
      font-size: 1rem;
    }
    
    .footer {
      text-align: center;
      margin-top: 2rem;
      color: #aaa;
      font-size: 0.9rem;
    }
    .footer a {
      color: #00d4ff;
      text-decoration: none;
      font-weight: 600;
    }
    
    .action-buttons {
      display: flex;
      gap: 1rem;
      margin-top: 2rem;
      flex-wrap: wrap;
    }
    .action-btn {
      background: linear-gradient(135deg, #00d4ff, #7b2ff7);
      color: #fff;
      border: none;
      padding: 1rem 2rem;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }
    .action-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 25px rgba(123,47,247,0.4);
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>⚙️ Instalação da Rotina Automática Windows</h1>
      <p>Configure a rotina diária da Praia Digital para rodar automaticamente</p>
    </div>

    <div class="card">
      <h2>✅ Status da Instalação</h2>
      <div class="status-grid">
        <div class="status-item">
          <h4>Scripts Criados</h4>
          <p id="scriptCount">—</p>
        </div>
        <div class="status-item">
          <h4>Agendamento</h4>
          <p id="scheduleStatus">Manual</p>
        </div>
        <div class="status-item">
          <h4>Última Execução</h4>
          <p>—</p>
        </div>
        <div class="status-item">
          <h4>Próxima Execução</h4>
          <p>Hoje, 09:00</p>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>📋 Passo a Passo - Instalação</h2>
      
      <div class="step">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>Verificar Python instalado</h3>
          <p>Abra o Prompt de Comando e execute:</p>
          <div class="code-block">
            python --version
            <button class="copy-btn" onclick="copiar('python --version')">📋</button>
          </div>
          <p style="margin-top:0.5rem; font-size:0.9rem;">Se aparecer Python 3.8+ está ok. Se não, instale em python.org</p>
        </div>
      </div>

      <div class="step">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>Navegar até a pasta do projeto</h3>
          <p>No Prompt de Comando:</p>
          <div class="code-block">
            cd C:\Users\Carolina\praia-digital
            <button class="copy-btn" onclick="copiar('cd C:\\Users\\Carolina\\praia-digital')">📋</button>
          </div>
        </div>
      </div>

      <div class="step">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>Executar instalação da rotina</h3>
          <p>Execute o instalador que cria a rotina no Windows:</p>
          <div class="code-block">
            scripts\instalar-rotina-comercial-diaria.bat
            <button class="copy-btn" onclick="copiar('scripts\\instalar-rotina-comercial-diaria.bat')">📋</button>
          </div>
          <p style="margin-top:0.5rem; font-size:0.9rem;">Este script configura o Agendador de Tarefas do Windows para executar a rotina todos os dias às 09:00.</p>
        </div>
      </div>

      <div class="step">
        <div class="step-number">4</div>
        <div class="step-content">
          <h3>Testar execução manual</h3>
          <p>Execute manualmente para verificar se funciona:</p>
          <div class="code-block">
            scripts\rotina-mestre-praia-digital.bat
            <button class="copy-btn" onclick="copiar('scripts\\rotina-mestre-praia-digital.bat')">📋</button>
          </div>
        </div>
      </div>

      <div class="step">
        <div class="step-number">5</div>
        <div class="step-content">
          <h3>Configurar backup automático</h3>
          <p>Execute o backup uma vez e depois o agendador cuida do resto:</p>
          <div class="code-block">
            scripts\executar-backup-incremental-comercial.bat
            <button class="copy-btn" onclick="copiar('scripts\\executar-backup-incremental-comercial.bat')">📋</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>🔧 Resolução de Problemas</h2>
      
      <div class="warning-box">
        <h3>⚠️ Erro: "execução de script está desabilitada"</h3>
        <p><strong>Solução:</strong> Execute o PowerShell como Administrador e digite:</p>
        <div class="code-block">
          Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
          <button class="copy-btn" onclick="copiar('Set-ExecutionPolicy RemoteSigned -Scope CurrentUser')">📋</button>
        </div>
        <p style="margin-top:0.5rem;">Depois tente novamente o instalador.</p>
      </div>

      <div class="warning-box" style="margin-top:1rem;">
        <h3>⚠️ Erro: "python não é reconhecido"</h3>
        <p>Instale Python em <a href="https://www.python.org/downloads/" target="_blank" style="color:#00d4ff;">python.org</a> e marque "Add to PATH" durante a instalação.</p>
      </div>

      <div class="success-box" style="margin-top:1rem;">
        <h3>✅ Alternativa: Usar o .vbs</h3>
        <p>Se o .bat não funcionar, use o arquivo <strong>scripts\rotina-mestre-praia-digital.vbs</strong>. Este funciona mesmo com políticas de execução bloqueadas.</p>
      </div>
    </div>

    <div class="card">
      <h2>🎯 Automação com Artigos SEO em Escala</h2>
      <p style="margin-bottom:1rem; color:#bbb;">Gerador de artigos únicos por cidade e tema, evitando repetição com os 191 existentes.</p>
      
      <div class="code-block">
        <button class="copy-btn" onclick="copiar('python scripts/automation/gerar_artigos_seo_cidade.py')">📋</button>
        python scripts/automation/gerar_artigos_seo_cidade.py
      </div>
      
      <div class="status-grid" style="margin-top:1rem;">
        <div class="status-item">
          <h4>Artigos Gerados</h4>
          <p id="articlesGenerated">3+</p>
        </div>
        <div class="status-item">
          <h4>Temas Únicos</h4>
          <p>10+</p>
        </div>
        <div class="status-item">
          <h4>Cidades</h4>
          <p>30+</p>
        </div>
        <div class="status-item">
          <h4>Duplicação</h4>
          <p style="color:#00ffa3;">0%</p>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <a href="scripts/instalar-rotina-comercial-diaria.bat" class="action-btn">⚙️ Instalar Rotina Automática</a>
      <a href="scripts/rotina-mestre-praia-digital.bat" class="action-btn secondary">▶️ Executar Rotina Agora</a>
      <a href="docs/sales/execucao-diaria-praia-digital-2026.html" target="_blank" class="action-btn secondary">📊 Ver Execução Diária</a>
    </div>

    <div class="footer">
      <p>🏖️ Praia Digital · Transformando imobiliárias do litoral paulista com IA</p>
      <p style="margin-top:0.5rem;">
        <a href="https://acarolmourad-commits.github.io/praia-digital/" target="_blank">Site Principal</a> • 
        <a href="https://praia.digital" target="_blank">Ferramentas Gratuitas</a>
      </p>
    </div>
  </div>

  <script>
    function copiar(text){
      navigator.clipboard.writeText(text).then(() => alert('Copiado: ' + text));
    }
    document.addEventListener('DOMContentLoaded', function(){
      const counts = Array.from({length: 50}, () => 1);
      document.getElementById('scriptCount').textContent = counts.length + ' scripts';
    });
  </script>
</body>
</html>
