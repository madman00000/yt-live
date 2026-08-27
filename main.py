import os, subprocess, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

STREAM_KEY = os.environ.get("STREAM_KEY")
VIDEO_ID = "1TK7wqyJ2uh_8Y7mBaxIIBBQGD0MpxhB4"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live running 24/7 - FIXED")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        return

def run_server():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

print("Downloading video...", flush=True)
os.system("pip install -q gdown")
# FIXED download command
os.system(f"gdown https://drive.google.com/uc?id={VIDEO_ID} -O video.mp4 --fuzzy")
print(f"File exists: {os.path.exists('video.mp4')}", flush=True)

if not os.path.exists('video.mp4'):
    print("ERROR: video.mp4 not found! Retrying with direct ID...", flush=True)
    os.system(f"gdown {VIDEO_ID} -O video.mp4 --fuzzy")
    print(f"Retry File exists: {os.path.exists('video.mp4')}", flush=True)

if not os.path.exists('video.mp4'):
    print("FATAL: Download failed - check Google Drive share!", flush=True)
    time.sleep(1000)

print("Starting FFmpeg to YouTube...", flush=True)
while True:
    try:
        if not STREAM_KEY:
            print("ERROR: STREAM_KEY not set!", flush=True)
            time.sleep(10)
            continue
        cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c:v libx264 -preset veryfast -b:v 1500k -maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Restart: {e}", flush=True)
        time.sleep(5)
