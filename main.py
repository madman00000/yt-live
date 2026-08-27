import os, subprocess, time, threading
from flask import Flask
app=Flask(__name__)
@app.route('/')
def home(): return "1080p HD LIVE"
def web(): app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
def stream():
    while True:
        k=os.environ.get("STREAM_KEY","").strip()
        if len(k)<10: time.sleep(10); continue
        print("Starting 1080p HD stream...")
        cmd=["ffmpeg","-re","-f","lavfi","-i","testsrc=s=1920x1080:r=30",
             "-f","lavfi","-i","sine=f=1000",
             "-c:v","libx264","-preset","ultrafast","-b:v","4000k","-maxrate","4000k",
             "-pix_fmt","yuv420p","-g","60","-c:a","aac","-b:a","128k",
             "-f","flv",f"rtmp://a.rtmp.youtube.com/live2/{k}"]
        subprocess.run(cmd)
        time.sleep(2)
threading.Thread(target=web,daemon=True).start()
stream()
