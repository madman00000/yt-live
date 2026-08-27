import os, subprocess, time, threading
from flask import Flask
app=Flask(__name__)
@app.route('/')
def home(): return "HD LIVE - YOUR VIDEO"
def web(): app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
def stream():
    while True:
        k=os.environ.get("STREAM_KEY","").strip()
        if len(k)<10: time.sleep(10); continue
        v="https://files.catbox.moe/1rqe5y.mp4"
        print("Streaming YOUR video in HD - copy mode (no buffering)")
        cmd=["ffmpeg","-re","-stream_loop","-1","-i",v,
             "-c:v","copy","-c:a","aac","-b:a","128k",
             "-f","flv",f"rtmp://a.rtmp.youtube.com/live2/{k}"]
        subprocess.run(cmd)
        time.sleep(3)
threading.Thread(target=web,daemon=True).start()
stream()
