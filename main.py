import os, subprocess, time, threading
from flask import Flask
app=Flask(__name__)
@app.route('/')
def home(): return "LIVE OK"
def web(): app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
def stream():
    while True:
        k=os.environ.get("STREAM_KEY","").strip()
        print(f"KEY LEN={len(k)}")
        if len(k)<10:
            print("NO KEY! Add STREAM_KEY in Render Environment")
            time.sleep(10); continue
        v=os.environ.get("VIDEO_URL","https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
        print("Starting YouTube RTMP...")
        cmd=["ffmpeg","-re","-stream_loop","-1","-i",v,"-c:v","libx264","-preset","veryfast","-b:v","4500k","-maxrate","5000k","-bufsize","8000k","-pix_fmt","yuv420p","-g","60","-c:a","aac","-b:a","128k","-ar","44100","-f","flv",f"rtmp://a.rtmp.youtube.com/live2/{k}"]
        subprocess.run(cmd)
        time.sleep(2)
threading.Thread(target=web,daemon=True).start()
stream()
