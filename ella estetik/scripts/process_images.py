import os
from PIL import Image

image_mapping = [
    ("assets/images/raw/photo_09.jpg", "salon-ic-mekan"),
    ("assets/images/raw/photo_08.jpg", "cilt-bakimi-led-terapi"),
    ("assets/images/raw/photo_04.jpg", "cilt-bakimi-karbon-peeling"),
    ("assets/images/raw/photo_02.jpg", "cilt-bakimi-goz-terapi"),
    ("assets/images/raw/photo_03.jpg", "protez-tirnak-mavi"),
    ("assets/images/raw/photo_07.jpg", "protez-tirnak-nailart"),
    ("assets/images/raw/photo_10.jpg", "protez-tirnak-kirmizi"),
    ("assets/images/raw/photo_01.jpg", "ipek-kirpik-kas-laminasyon"),
    ("assets/images/raw/photo_06.jpg", "ipek-kirpik-uygulama"),
    ("assets/images/canva_raw/canva_logo_or_asset.png", "sac-simulasyonu"),
    ("assets/images/canva_raw/canva_01.jpg", "lazer-epilasyon-banner"),
    ("assets/images/canva_raw/canva_03.jpg", "cilt-bakimi-hydrafacial"),
]

os.makedirs("assets/images", exist_ok=True)

processed = []

for src, slug in image_mapping:
    if not os.path.exists(src):
        print(f"File not found: {src}")
        continue
    with Image.open(src) as img:
        # Convert RGBA to RGB if needed
        if img.mode in ("RGBA", "P"):
            rgb_img = img.convert("RGB")
        else:
            rgb_img = img.convert("RGB")
        
        # Max dimension 1920
        w, h = rgb_img.size
        if max(w, h) > 1920:
            scale = 1920 / max(w, h)
            new_w, new_h = int(w * scale), int(h * scale)
            rgb_img = rgb_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        webp_path = f"assets/images/{slug}.webp"
        jpg_path = f"assets/images/{slug}.jpg"
        
        # Save WebP
        rgb_img.save(webp_path, "WEBP", quality=85, method=6)
        # Save JPG fallback
        rgb_img.save(jpg_path, "JPEG", quality=85, optimize=True)
        
        webp_size = os.path.getsize(webp_path)
        jpg_size = os.path.getsize(jpg_path)
        print(f"Processed {slug}: WebP={webp_size//1024}KB, JPG={jpg_size//1024}KB ({rgb_img.size[0]}x{rgb_img.size[1]})")
        
        processed.append({
            "name": slug,
            "webp": webp_path,
            "jpg": jpg_path,
            "width": rgb_img.size[0],
            "height": rgb_img.size[1]
        })

print(f"Total processed images: {len(processed)}")
