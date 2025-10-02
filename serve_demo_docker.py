#!/usr/bin/env python3
import http.server
import socketserver
import json
import time
import os

PORT = int(os.environ.get('PORT', 8080))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-typesense-api-key')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            health_data = {'status': 'healthy', 'timestamp': time.time(), 'service': 'enfue-search-demo'}
            self.wfile.write(json.dumps(health_data).encode())
            return
        
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', '/index.html')
            self.end_headers()
            return
        
        super().do_GET()

if __name__ == "__main__":
    # Setup Typesense data on startup
    try:
        print("📊 Setting up Typesense data...")
        import subprocess
        result = subprocess.run(["python", "setup_typesense.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Data import completed")
        else:
            print("⚠️ Data import failed, continuing anyway...")
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Data import failed: {e}")
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        httpd.serve_forever()
