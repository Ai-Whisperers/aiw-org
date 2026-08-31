#!/usr/bin/env python3
"""admin-server.py - Simple HTTP server for the AIW admin dashboard.

Serves:
- / -> admin dashboard HTML
- /org-state.json -> current org state
- /cost-tracker.json -> cost data
- /dashboard/all -> all-route markdown output

Default port: 8090
"""
import http.server
import socketserver
import subprocess
from pathlib import Path

STATE_DIR = Path("/opt/data/state")
DASHBOARD_DIR = Path("/opt/data/build/aiw-admin")
PORT = 8090


class AdminHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/org-state.json":
            return self._serve_file(STATE_DIR / "org-state.json")
        if self.path == "/cost-tracker.json":
            return self._serve_file(STATE_DIR / "cost-tracker.json")
        if self.path == "/errors.json":
            return self._serve_file(STATE_DIR / "errors.json")
        if self.path.startswith("/dashboard/"):
            route = self.path.replace("/dashboard/", "")
            return self._serve_route(route if route != "all" else None)
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def _serve_file(self, path):
        if not path.exists():
            self.send_error(404, "Not found")
            return
        try:
            content = path.read_bytes()
            self.send_response(200)
            if path.suffix == ".json":
                self.send_header("Content-Type", "application/json")
            else:
                self.send_header("Content-Type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

    def _serve_route(self, route=None):
        cmd = ["python3", "/opt/data/agents-v2/scripts/dashboard/org-dashboard.py"]
        if route:
            cmd.append(route)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            content = r.stdout.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

    def log_message(self, format, *args):
        pass


def main():
    with socketserver.TCPServer(("", PORT), AdminHandler) as httpd:
        print(f"Admin dashboard listening on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AIW Admin Dashboard Server")
    parser.add_argument("--port", type=int, default=8090, help="Port to listen on")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()
    PORT = args.port
    main()
