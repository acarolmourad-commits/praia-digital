const http = require('http');
const fs = require('fs');
const path = require('path');

const API_DIR = path.join(__dirname, 'api');

function sendJson(res, statusCode, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function tryStaticApi(reqPath) {
  const safe = path.normalize(reqPath).replace(/^\.\//, '').replace(/\/g, '/');
  const full = path.join(API_DIR, safe);
  if (!full.startsWith(API_DIR)) return null;
  if (!fs.existsSync(full) || !fs.statSync(full).isFile()) return null;
  const body = fs.readFileSync(full, 'utf8');
  const ext = path.extname(full).toLowerCase();
  const ct = ext === '.js' ? 'application/javascript' : ext === '.json' ? 'application/json' : ext === '.html' ? 'text/html' : 'application/octet-stream';
  return { body, ct };
}

function createFakeRes(res) {
  let statusCode = 200;
  const headers = {};
  return {
    setHeader(k, v) { headers[k] = v; },
    getHeader(k) { return headers[k]; },
    status(code) { statusCode = code; return this; },
    json(obj) { sendJson(res, statusCode, obj); },
    end(payload) {
      const ct = headers['Content-Type'] || 'application/json';
      res.writeHead(statusCode, Object.assign({ 'Access-Control-Allow-Origin': '*', 'Cache-Control': 'no-store' }, headers));
      res.end(typeof payload === 'string' ? payload : JSON.stringify(payload));
    }
  };
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://' + req.headers.host);
  const reqPath = decodeURIComponent(url.pathname);

  if (reqPath === '/health' || reqPath === '/health/') {
    return sendJson(res, 200, { status: 'ok', env: 'local-adapter' });
  }

  if (reqPath.startsWith('/backend/api/')) {
    const rel = reqPath.slice('/backend/api/'.length);

    if (req.method === 'OPTIONS') {
      res.writeHead(204, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'no-store'
      });
      return res.end();
    }

    if (req.method === 'POST' && new RegExp('^leads/(b2b|report|index)\.js$').test(rel)) {
      let body = '';
      req.setEncoding('utf8');
      for await (const chunk of req) body += chunk;
      let parsed = {};
      try { parsed = body ? JSON.parse(body) : {}; } catch {}

      const modPath = path.join(API_DIR, rel);
      try {
        const handler = require(modPath);
        const fakeReq = { method: 'POST', body: parsed, headers: req.headers };
        await handler(fakeReq, createFakeRes(res));
        return;
      } catch (err) {
        return sendJson(res, 500, { error: 'handler_error', detail: err.message });
      }
    }

    const staticFile = tryStaticApi(rel);
    if (staticFile) {
      res.writeHead(200, {
        'Content-Type': staticFile.ct,
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-store'
      });
      return res.end(staticFile.body);
    }

    return sendJson(res, 404, { error: 'not_found', path: rel });
  }

  if (req.method === 'GET' && (reqPath === '/' || reqPath === '/index.html')) {
    const indexHtml = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
    return res.end(indexHtml);
  }

  return sendJson(res, 404, { error: 'not_found', path: reqPath });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log('Backend adapter listening on http://localhost:' + PORT);
});
