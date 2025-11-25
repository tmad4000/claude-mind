#!/usr/bin/env python3
"""
Simple search server for claude-mind content.
Provides JSON API for searching across all markdown and code files.

Run: python3 search_server.py
Then access: http://localhost:8081/search?q=meditation
"""

import http.server
import socketserver
import json
import os
import re
from urllib.parse import urlparse, parse_qs
from pathlib import Path

PORT = 8081
BASE_DIR = Path(__file__).parent.parent

# File extensions to search
SEARCHABLE = ['.md', '.py', '.json', '.html', '.js', '.txt']

# Files/dirs to skip
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.pytest_cache'}

def search_files(query, max_results=50):
    """Search all files for query, return matches with context."""
    results = []
    query_lower = query.lower()
    query_pattern = re.compile(re.escape(query), re.IGNORECASE)

    for root, dirs, files in os.walk(BASE_DIR):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not any(fname.endswith(ext) for ext in SEARCHABLE):
                continue

            fpath = Path(root) / fname
            rel_path = fpath.relative_to(BASE_DIR)

            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Find all matches
                for i, line in enumerate(content.split('\n'), 1):
                    if query_lower in line.lower():
                        # Extract context
                        match = query_pattern.search(line)
                        if match:
                            results.append({
                                'file': str(rel_path),
                                'line': i,
                                'text': line.strip()[:200],
                                'highlight_start': match.start(),
                                'highlight_end': match.end()
                            })

                            if len(results) >= max_results:
                                return results

            except Exception as e:
                pass  # Skip files that can't be read

    return results

class SearchHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/search':
            params = parse_qs(parsed.query)
            query = params.get('q', [''])[0]

            if not query:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing query parameter q'}).encode())
                return

            results = search_files(query)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'query': query,
                'count': len(results),
                'results': results
            }).encode())

        elif parsed.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
<!DOCTYPE html>
<html>
<head>
    <title>Claude Mind Search</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #1e293b; color: #e2e8f0; }
        input { width: 100%; padding: 12px; font-size: 16px; border: 2px solid #3b82f6; border-radius: 8px; background: #0f172a; color: #e2e8f0; }
        .result { margin: 15px 0; padding: 15px; background: #0f172a; border-radius: 8px; border-left: 3px solid #3b82f6; }
        .file { color: #60a5fa; font-weight: bold; }
        .line { color: #94a3b8; font-size: 0.9em; }
        .text { margin-top: 5px; font-family: monospace; word-break: break-all; }
        mark { background: #eab308; color: #000; padding: 0 2px; }
        a { color: #60a5fa; text-decoration: none; }
    </style>
</head>
<body>
    <h1>Claude Mind Search</h1>
    <input type="text" id="q" placeholder="Search all files..." autofocus>
    <div id="results"></div>
    <script>
        const input = document.getElementById('q');
        const results = document.getElementById('results');
        let timeout;
        input.addEventListener('input', () => {
            clearTimeout(timeout);
            timeout = setTimeout(async () => {
                const q = input.value.trim();
                if (!q) { results.innerHTML = ''; return; }
                const res = await fetch('/search?q=' + encodeURIComponent(q));
                const data = await res.json();
                results.innerHTML = `<p>Found ${data.count} results</p>` +
                    data.results.map(r => `
                        <div class="result">
                            <div class="file"><a href="/demos/viewer.html?file=${r.file}" target="_blank">${r.file}</a></div>
                            <div class="line">Line ${r.line}</div>
                            <div class="text">${r.text.substring(0, r.highlight_start)}<mark>${r.text.substring(r.highlight_start, r.highlight_end)}</mark>${r.text.substring(r.highlight_end)}</div>
                        </div>
                    `).join('');
            }, 300);
        });
    </script>
</body>
</html>
            ''')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Quiet logging

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), SearchHandler) as httpd:
        print(f"Search server at http://localhost:{PORT}")
        print(f"API: http://localhost:{PORT}/search?q=your+query")
        httpd.serve_forever()
