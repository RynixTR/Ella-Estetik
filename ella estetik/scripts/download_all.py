import os
import json
import urllib.request
from PIL import Image

with open("maps_photo_keys.json", encoding="utf-8") as f:
    photo_urls = json.load(f)

os.makedirs("assets/images/raw", exist_ok=True)

downloaded = []
for i, base_url in enumerate(photo_urls):
    # Request high resolution image (s1600)
    full_url = f"{base_url}=s1600"
    file_path = f"assets/images/raw/photo_{i+1:02d}.jpg"
    print(f"Downloading photo {i+1}...")
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp, open(file_path, "wb") as f_out:
            f_out.write(resp.read())
        
        with Image.open(file_path) as img:
            w, h = img.size
            fmt = img.format
            print(f" -> Saved {file_path}: {w}x{h} ({fmt})")
            downloaded.append({
                "id": i + 1,
                "file": file_path,
                "width": w,
                "height": h,
                "aspect_ratio": round(w / h, 2),
                "url": full_url
            })
    except Exception as e:
        print(f"Error downloading photo {i+1}: {e}")

with open("downloaded_photos.json", "w", encoding="utf-8") as f:
    json.dump(downloaded, f, indent=2)

print("Done! Total downloaded:", len(downloaded))
