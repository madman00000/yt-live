import os, subprocess, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

STREAM_KEY = os.environ.get("cd7g-1u66-hgfs-ghbh-6yge")
VIDEO_ID = "https://drive.google.com/file/d/1TK7WyqJ2uh_8Y7wBaxTIBBQGD0MpxhB4/view?usp=sharing"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live running 24/7")

def run_server():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

print("Downloading video...")
os.system("pip install gdown -q")
os.system(f"gdown --id {VIDEO_ID} -O video.mp4")
print(f"File exists: {os.path.exists('video.mp4')}")

while True:
    try:
        cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c:v libx264 -preset veryfast -b:v 1500k -maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Restart: {e}")
        time.sleep(5)
