import os
import urllib.request
from PIL import Image

canva_urls = {
    "canva_01.jpg": "https://ellaestetik.my.canva.site/_assets/media/5ef1ae2ad787092525d828669bb4bf6c.jpg",
    "canva_02.jpg": "https://ellaestetik.my.canva.site/_assets/media/29d12a3f802249e2edb49b9e57d69d7f.jpg",
    "canva_03.jpg": "https://ellaestetik.my.canva.site/_assets/media/1b82d28fc8e696a6564b1c2b946b0827.jpg",
    "canva_logo_or_asset.png": "https://ellaestetik.my.canva.site/_assets/media/e4e7fec70206753e162de8f652f6ee43.png",
}

os.makedirs("assets/images/canva_raw", exist_ok=True)
for name, u in canva_urls.items():
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        path = f"assets/images/canva_raw/{name}"
        with urllib.request.urlopen(req, timeout=10) as r, open(path, "wb") as f:
            f.write(r.read())
        with Image.open(path) as img:
            print(f"Saved {name}: {img.size} ({img.format})")
    except Exception as e:
        print(f"Error {name}: {e}")
