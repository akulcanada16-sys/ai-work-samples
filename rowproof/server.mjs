import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const root = process.cwd();
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml' };
createServer(async (req, res) => {
  const requestPath = req.url === '/' ? '/index.html' : req.url.split('?')[0];
  const file = normalize(join(root, requestPath));
  if (!file.startsWith(root)) { res.writeHead(403); return res.end('Forbidden'); }
  try { const content = await readFile(file); res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' }); res.end(content); }
  catch { res.writeHead(404); res.end('Not found'); }
}).listen(4173, () => console.log('RowProof running at http://localhost:4173'));
