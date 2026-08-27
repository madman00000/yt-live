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
    print(f"Downloading {id}...", flush=True)
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

if not os.path.exists("video.mp4"):
    download_drive(VIDEO_ID, "video.mp4")

size = os.path.getsize("video.mp4")/1024/1024
print(f"Video size: {size:.2f} MB", flush=True)

print("Starting 720p Low-Memory Live...", flush=True)
while True:
    # SCALED TO 720p, low bitrate, low memory
    cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -vf "scale=1280:720" -c:v libx264 -preset ultrafast -b:v 1000k -maxrate 1000k -bufsize 2000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 96k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
    subprocess.run(cmd, shell=True)
    print("Restarting...", flush=True)
    time.sleep(5)
