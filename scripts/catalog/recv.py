"""临时本地接收器:接收浏览器 POST 过来的指标 JSON,写成 CSV。
用法:.venv-api\\Scripts\\python scripts\\catalog\\recv.py
浏览器侧 fetch('http://127.0.0.1:8799/save', {method:'POST', body: JSON.stringify({name, rows})})
"""
import csv
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "docs", "catalog", "em")
os.makedirs(OUT, exist_ok=True)

HEADERS = {
    "csd": ["品种id", "分类id", "指标代码", "指标中文名", "单位", "参数", "适用范围"],
    "ctr": ["品种", "报表名", "报表代码CtrName", "字段代码", "字段中文名"],
    "css": ["品种", "分类", "指标代码", "指标中文名", "单位", "参数", "适用范围"],
}


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(n).decode("utf-8"))
        name = payload["name"]
        rows = payload["rows"]
        path = os.path.join(OUT, f"{name}_indicators.csv")
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(HEADERS.get(name, []))
            w.writerows(rows)
        print(f"saved {name}: {len(rows)} rows -> {path}")
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "rows": len(rows)}).encode())

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("listening on http://127.0.0.1:8799 ... Ctrl+C to stop")
    HTTPServer(("127.0.0.1", 8799), Handler).serve_forever()
