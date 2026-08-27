import os, subprocess, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

STREAM_KEY = os.environ.get("STREAM_KEY")
VIDEO_ID = "1TK7WyqJ2uh_8Y7wBaxTIBBQGD0MpxhB4"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live Running")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        return

def run_server():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

print(f"=== DOWNLOADING {VIDEO_ID} ===", flush=True)

# Method 1: Python gdown with fuzzy - handles big files
import gdown
try:
    gdown.download(id=VIDEO_ID, output="video.mp4", quiet=False, fuzzy=True, use_cookies=False)
except Exception as e:
    print(f"Method1 error: {e}", flush=True)

# If still fails, try direct URL with cookies bypass
if not os.path.exists("video.mp4") or os.path.getsize("video.mp4") < 1000:
    print("Trying direct download bypass...", flush=True)
    try:
        gdown.download(url=f"https://drive.google.com/uc?id={VIDEO_ID}", output="video.mp4", quiet=False, fuzzy=True)
    except Exception as e:
        print(f"Method2 error: {e}", flush=True)

exists = os.path.exists("video.mp4")
size = os.path.getsize("video.mp4") if exists else 0
print(f"=== RESULT Exists={exists} Size={size/1024/1024:.2f} MB ===", flush=True)

if not exists or size < 10000:
    print("FAILED - File too big or not public!", flush=True)
    print("SOLUTION: Re-upload video smaller than 90MB!", flush=True)
    os.system("ls -lh")
    time.sleep(9999)

print("=== STARTING LIVE ===", flush=True)
while True:
    cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c:v libx264 -preset veryfast -b:v 1500k -maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
    subprocess.run(cmd, shell=True)
    time.sleep(5)
