import os, subprocess, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

STREAM_KEY = os.environ.get("STREAM_KEY")
VIDEO_ID = "1TK7WyqJ2uh_8Y7wBaxTIBBQGD0MpxhB4"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live")
    def log_message(self, *a): return
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), Handler).serve_forever()
threading.Thread(target=run_server, daemon=True).start()

def dl(id, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1_000_000: return
    URL = "https://drive.google.com/uc?export=download"
    s = requests.Session()
    r = s.get(URL, params={'id': id}, stream=True)
    token = next((v for k,v in r.cookies.items() if k.startswith('download_warning')), None)
    if token: r = s.get(URL, params={'id': id, 'confirm': token}, stream=True)
    with open(dest, "wb") as f:
        for c in r.iter_content(32768):
            if c: f.write(c)

dl(VIDEO_ID, "video.mp4")
print("Streaming original quality (copy) - 1440p", flush=True)

while True:
    # COPY = Original 1440p quality, no CPU, no low quality!
    cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c copy -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
    subprocess.run(cmd, shell=True)
    time.sleep(2)
