import json
import requests

with open("captured_videos.json", encoding="utf-8") as f:
    urls = json.load(f)

print(f"Captured video URLs count: {len(urls)}")
for u in urls:
    if "videoplayback" in u and "video/mp4" in u:
        print("Trying url:", u[:100])
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Origin": "https://www.google.com"
        }
        res = requests.get(u, headers=headers, stream=True, timeout=15)
        print("Status code:", res.status_code, "Content-Length:", res.headers.get("Content-Length"))
        if res.status_code == 200:
            with open("assets/videos/cilt-bakimi-uygulama.mp4", "wb") as f:
                for chunk in res.iter_content(chunk_size=1024*64):
                    if chunk:
                        f.write(chunk)
            print("Successfully saved assets/videos/cilt-bakimi-uygulama.mp4!")
            break
