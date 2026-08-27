import os, subprocess, time, threading
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

print(f"Downloading {VIDEO_ID} (17.7MB)...", flush=True)
import gdown
gdown.download(id=VIDEO_ID, output="video.mp4", quiet=False, fuzzy=True)

import pathlib
size = pathlib.Path("video.mp4").stat().st_size if pathlib.Path("video.mp4").exists() else 0
print(f"Downloaded: {size/1024/1024:.2f} MB", flush=True)

print("Starting 24/7 Loop Live...", flush=True)
while True:
    cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c:v libx264 -preset veryfast -b:v 2500k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
    subprocess.run(cmd, shell=True)
    time.sleep(3)
