import argparse
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .app import MAX_BODY, WEB, analyze, parse_request
from .fixtures import make_dial
import cv2
import base64


class Handler(BaseHTTPRequestHandler):
    def respond(self, code, data, content_type='application/json'):
        raw = data if isinstance(data, bytes) else json.dumps(data, allow_nan=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        routes = {'/': ('index.html','text/html; charset=utf-8'),
                  '/app.js': ('app.js','text/javascript'), '/style.css': ('style.css','text/css')}
        if self.path in routes:
            name, mime = routes[self.path]
            return self.respond(200, (WEB/name).read_bytes(), mime)
        if self.path == '/health':
            return self.respond(200, {'ok': True, 'opencv_version': cv2.__version__, 'mode': 'local'})
        if self.path.startswith('/sample/'):
            condition = self.path.split('/')[-1]
            if condition not in ('clean','blur','ambiguous','missing','dim','noise','high'):
                return self.respond(404, {'error':'Unknown sample'})
            frame = make_dial(90 if condition == 'high' else 62, condition=condition)
            return self.respond(200, cv2.imencode('.png', frame)[1].tobytes(), 'image/png')
        return self.respond(404, {'error': 'Not found'})

    def do_POST(self):
        if self.path != '/api/inspect':
            return self.respond(404, {'error':'Not found'})
        token = os.environ.get('DIALGUARD_TOKEN')
        if token and not hmac.compare_digest(self.headers.get('X-DialGuard-Token',''),token):
            return self.respond(401, {'error':'Invalid demo access code'})
        try:
            length = int(self.headers.get('Content-Length','0'))
            if length < 1 or length > MAX_BODY:
                return self.respond(413, {'error':'Request too large or empty'})
            result = analyze(parse_request(self.rfile.read(length)))
            return self.respond(200, result)
        except (ValueError, TypeError) as exc:
            return self.respond(400, {'error':str(exc)})
        except Exception:
            return self.respond(500, {'error':'Inspection failed; no reading recorded'})

    def log_message(self, fmt, *args):
        # Only request line/status, never access codes or uploaded images.
        super().log_message(fmt, *args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    print(f'DialGuard: http://{args.host}:{args.port}', flush=True)
    ThreadingHTTPServer((args.host,args.port), Handler).serve_forever()

if __name__ == '__main__':
    main()
