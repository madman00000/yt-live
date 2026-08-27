import os, subprocess, time, threading
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "HD LIVE - YOUR VIDEO - 30 DAYS"

def web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def stream():
    while True:
        k = os.environ.get("STREAM_KEY","").strip()
        if len(k) < 10:
            print("Waiting for STREAM_KEY...")
            time.sleep(10)
            continue
        
        video = "https://files.catbox.moe/1rqe5y.mp4"
        print(f"Streaming YOUR video: {video}")
        
        # COPY mode = 0 CPU = No buffering = Perfect for Render FREE
        cmd = [
            "ffmpeg", "-re", "-stream_loop", "-1",
            "-i", video,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "flv",
            f"rtmp://a.rtmp.youtube.com/live2/{k}"
        ]
        
        subprocess.run(cmd)
        print("FFmpeg ended, restarting in 3s...")
        time.sleep(3)

threading.Thread(target=web, daemon=True).start()
stream()
