import os, subprocess, time, threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Live Streaming is Running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def run_stream():
    while True:
        try:
            key = os.environ.get("STREAM_KEY")
            if not key:
                print("No STREAM_KEY!")
                time.sleep(10)
                continue
            
            url = os.getenv("VIDEO_URL", "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4")
            
            print("Starting 1440p copy stream...")
            cmd = [
                "ffmpeg", "-re", "-stream_loop", "-1",
                "-i", url,
                "-c:v", "copy",  # No re-encode = original 1440p quality!
                "-c:a", "aac", "-b:a", "128k",
                "-f", "flv",
                f"rtmp://a.rtmp.youtube.com/live2/{key}"
            ]
            subprocess.run(cmd)
            print("FFmpeg ended, restarting in 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    run_stream()
