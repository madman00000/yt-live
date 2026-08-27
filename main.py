import os, subprocess, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

STREAM_KEY = os.environ.get("STREAM_KEY")
VIDEO_ID = "1TK7WyqJ2uh_8Y7wBaxTIBBQGD0MpxhB4"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, a, *b):
        return

def run_server():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def download_drive(id, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000000:
        print("Video already exists, skipping download", flush=True)
        return
    print("Downloading...", flush=True)
    URL = "https://drive.google.com/uc?export=download"
    s = requests.Session()
    r = s.get(URL, params={'id': id}, stream=True)
    token = None
    for k, v in r.cookies.items():
        if k.startswith('download_warning'):
            token = v
            break
    if token:
        r = s.get(URL, params={'id': id, 'confirm': token}, stream=True)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(32768):
            if chunk: f.write(chunk)

download_drive(VIDEO_ID, "video.mp4")
print(f"Size: {os.path.getsize('video.mp4')/1024/1024:.1f} MB - Original Quality", flush=True)

while True:
    # COPY MODE - No re-encode = 2K quality + No CPU + No buffering!
    cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c:v copy -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
    subprocess.run(cmd, shell=True)
    time.sleep(3)
