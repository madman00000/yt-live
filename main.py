import os, subprocess, time, threading
from flask import Flask
app=Flask(__name__)
@app.route('/')
def home(): return "LIVE 1440p OK"
def web(): app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
def stream():
    while True:
        k=os.environ.get("STREAM_KEY","").strip()
        if len(k)<10:
            print("NO KEY"); time.sleep(10); continue
        print("Starting 1440p stream to YouTube...")
        cmd=["ffmpeg","-re","-f","lavfi","-i","testsrc=s=2560x1440:r=30",
             "-f","lavfi","-i","sine=f=1000",
             "-c:v","libx264","-preset","veryfast","-b:v","6000k",
             "-c:a","aac","-f","flv",f"rtmp://a.rtmp.youtube.com/live2/{k}"]
        subprocess.run(cmd)
        time.sleep(2)
threading.Thread(target=web,daemon=True).start()
stream()
