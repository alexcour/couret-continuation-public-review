"""Controlled permission-workflow fixture, exposed through a separate HTTP process.

    This module is NOT imported by the diagnostic engine. Fresh preparation is a
    test-fixture facility, not a claim that a production API can be reset.
    The independently specified bound is four: two mutable boolean fields.
"""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import secrets


class Workflow:
    def __init__(self, variant='reference'):
        self.locked = False
        self.approved = False
        self.variant = variant

    @property
    def view(self):
        return 'LOCKED' if self.locked else 'READY'

    def step(self, action):
        decision = 'ACK'
        if action == 'APPROVE':
            self.approved = True
        elif action == 'EDIT':
            if self.variant != 'stale_approval':
                self.approved = False
        elif action == 'FAULT':
            self.locked = True
        elif action == 'REARM':
            self.locked = False
        elif action == 'COMMIT':
            if self.locked:
                decision = 'BLOCKED_LOCK'
            elif not self.approved:
                decision = 'BLOCKED_REVIEW'
            else:
                decision = 'COMMITTED'
                self.approved = False
        else:
            raise ValueError('Unknown action')
        return {'decision': decision, 'view': self.view}


def serve(port, variant):
    sessions = {}

    class Handler(BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.0'

        def log_message(self, *_):
            pass

        def respond(self, status, data):
            encoded = json.dumps(data).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_POST(self):
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if size < 0 or size > 10000:
                    raise ValueError('Invalid request size')
                body = json.loads(self.rfile.read(size))
                if not isinstance(body, dict):
                    raise ValueError('Expected JSON object')
                if self.path == '/prepare':
                    session = secrets.token_hex(12)
                    sessions[session] = Workflow(variant)
                    self.respond(200, {'session': session, 'view': sessions[session].view})
                elif self.path == '/step':
                    self.respond(200, sessions[body['session']].step(body['action']))
                elif self.path == '/release':
                    del sessions[body['session']]
                    self.respond(200, {'released': True})
                else:
                    self.respond(404, {'error': 'Unknown endpoint'})
            except (KeyError, TypeError, ValueError):
                self.respond(400, {'error': 'Invalid action or session'})

    with HTTPServer(('127.0.0.1', port), Handler) as server:
        print(json.dumps({'base_url': f'http://127.0.0.1:{server.server_port}',
                          'variant': variant}), flush=True)
        server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--variant', choices=['reference', 'stale_approval'], default='reference')
    args = parser.parse_args()
    serve(args.port, args.variant)
