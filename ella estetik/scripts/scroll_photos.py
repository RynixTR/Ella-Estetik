import os
import sys
import re
import time
import json
import urllib.request
from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.google.com/maps/place/Ella+Estetik+Ve+G%C3%BCzellik/@36.8703419,30.6281994,17z/data=!3m1!4b1!4m6!3m5!1s0x14c391652edb708b:0x9d1f75a00a75b3c7!8m2!3d36.8703419!4d30.6281994!16s%2Fg%2F11s3jxx422?entry=ttu&g_ep=EgoyMDI2MTEwNC4wIKXMDSoASAFQAw%3D%3D"

os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/videos", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        locale="tr-TR",
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    print("Loading Google Maps...")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(4)

    # Click on the photo button to open gallery
    photo_btn = page.locator("button[aria-label*='fotoğraf' i], button[aria-label*='Fotoğraflar' i]").first
    if not photo_btn.is_visible():
        photo_btn = page.locator("text='Fotoğraflar'").first
    photo_btn.click()
    time.sleep(3)

    # Find the photo gallery scroll container
    # Click inside the photo list pane to focus it
    page.mouse.click(500, 300)
    time.sleep(1)

    print("Scrolling to load photos...")
    for _ in range(25):
        page.keyboard.press("PageDown")
        time.sleep(0.3)

    time.sleep(2)
    html = page.content()
    
    # Check for videos
    video_elements = page.locator("video").all()
    print("Video tags found:", len(video_elements))

    browser.close()

# Extract all unique image URLs from HTML
matches = re.findall(r'https:\/\/lh3\.googleusercontent\.com\/gps-cs-s\/[A-Za-z0-9_\-]+', html)
unique_keys = list(dict.fromkeys(matches))
print(f"Extracted {len(unique_keys)} unique Google Maps photo IDs")

with open("maps_photo_keys.json", "w", encoding="utf-8") as f:
    json.dump(unique_keys, f, indent=2)
