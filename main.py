import os, subprocess, time, threading
from flask import Flask
app=Flask(__name__)
@app.route('/')
def home(): return "HD LIVE WITH YOUR VIDEO"
def web(): app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
def stream():
    while True:
        k=os.environ.get("STREAM_KEY","").strip()
        if len(k)<10:
            print("NO STREAM_KEY"); time.sleep(10); continue
        v="https://files.catbox.moe/1rqe5y.mp4"
        print(f"Starting HD stream with your video: {v}")
        # Try copy first (0% CPU = Best HD), if fails it auto re-encodes to 1080p HD
        cmd=["ffmpeg","-re","-stream_loop","-1","-i",v,
             "-c:v","copy","-c:a","aac","-b:a","128k",
             "-f","flv",f"rtmp://a.rtmp.youtube.com/live2/{k}"]
        p=subprocess.run(cmd)
        print("Copy failed, trying HD re-encode...")
        cmd2=["ffmpeg","-re","-stream_loop","-1","-i",v,
              "-c:v","libx264","-preset","veryfast","-b:v","4000k",
              "-pix_fmt","yuv420p","-g","60","-c:a","aac",
              "-f","flv",f"rtmp://a.rtmp.youtube.com/live2/{k}"]
        subprocess.run(cmd2)
        time.sleep(3)
threading.Thread(target=web,daemon=True).start()
stream()
