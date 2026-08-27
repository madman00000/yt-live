import os, subprocess, time

STREAM_KEY = os.environ.get("cd7g-1u66-hgfs-ghbh-6yge")
VIDEO_ID = "https://drive.google.com/file/d/1TK7WyqJ2uh_8Y7wBaxTIBBQGD0MpxhB4/view?usp=sharing"

print("Downloading video...")
os.system(f"pip install gdown -q && gdown https://drive.google.com/file/d/{VIDEO_ID}/view?usp=sharing --fuzzy -O video.mp4")
print("Download done!")

while True:
    try:
        cmd = f'ffmpeg -re -stream_loop -1 -i video.mp4 -c:v libx264 -preset veryfast -b:v 1500k -maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Restarting: {e}")
        time.sleep(5)
