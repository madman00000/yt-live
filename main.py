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
    def log_message(self, format, *args):
        return

def run_server():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def download_drive(id, dest):
    print(f"Direct downloading {id}...", flush=True)
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    r = session.get(URL, params={'id': id}, stream=True)
    token = None
    for k, v in r.cookies.items():
        if k.startswith('download_warning'):
            token = v
            break
    if token:
        r = session.get(URL, params={'id': id, 'confirm': token}, stream=True)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(32768):
            if chunk:
                f.write(chunk)
    print("Direct download done!", flush=True)

print("Downloading video...", flush=True)
download_drive(VIDEO_ID, "video.mp4")

import pathlib
size = pathlib.Path("video.mp4").stat().st_size if pathlib.Path("video.mp4").exists() else 0
print(f"Downloaded size: {size/1024/1024:.2f} MB", flush=True)

if size < 10000:
    print("Failed! Trying backup method...", flush=True)
    os.system(f"curl -L -o video.mp4 'https://drive.google.com/uc?export=download&id={VIDEO_ID}'")
    size = pathlib.Path("video.mp4").stat().st_size if pathlib.Path("video.mp4").exists() else 0
    print(f"After curl: {size/1024/1024:.2f} MB", flush=True)

print("Starting Live Loop...", flush=True)
while True:
    cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c:v libx264 -preset veryfast -b:v 2500k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
    subprocess.run(cmd, shell=True)
    time.sleep(3)
