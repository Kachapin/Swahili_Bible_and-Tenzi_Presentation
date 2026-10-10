import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

# In-memory storage for current display payload
current_state = json.dumps({"action": "hide", "timestamp": 0})

class TenziRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global current_state
        if self.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(current_state.encode('utf-8'))
        else:
            # Serves static files (controller.html, display.html, Tenzi_*.json)
            super().do_GET()

    def do_POST(self):
        global current_state
        if self.path == '/api/update':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            current_state = body.decode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, TenziRequestHandler)
    print("--------------------------------------------------")
    print(" Tenzi Custom Server Running on http://127.0.0.1:8000")
    print("--------------------------------------------------")
    httpd.serve_forever()