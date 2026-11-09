import os
import sys
import re
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.google.com/maps/place/Ella+Estetik+Ve+G%C3%BCzellik/@36.8703419,30.6281994,17z/data=!3m1!4b1!4m6!3m5!1s0x14c391652edb708b:0x9d1f75a00a75b3c7!8m2!3d36.8703419!4d30.6281994!16s%2Fg%2F11s3jxx422?entry=ttu&g_ep=EgoyMDI2MTEwNC4wIKXMDSoASAFQAw%3D%3D"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        locale="tr-TR",
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # Click on the photo button
    photo_btn = page.locator("button[aria-label*='fotoğraf' i], button[aria-label*='Fotoğraflar' i]").first
    if not photo_btn.is_visible():
        photo_btn = page.locator("text='Fotoğraflar'").first
    photo_btn.click()
    time.sleep(3)

    # Let's see what scrollable containers exist
    containers = page.locator("div.m6QErb").all()
    print(f"Found {len(containers)} m6QErb containers")
    
    # We can use page.mouse.wheel over the left panel (e.g. x=200, y=400)
    for step in range(15):
        page.mouse.move(250, 500)
        page.mouse.wheel(0, 3000)
        time.sleep(0.8)

    html = page.content()
    browser.close()

matches = re.findall(r'https:\/\/lh3\.googleusercontent\.com\/gps-cs-s\/[A-Za-z0-9_\-]+', html)
unique_keys = list(dict.fromkeys(matches))
print(f"Total unique photo IDs found after wheel scrolling: {len(unique_keys)}")
with open("maps_photo_keys.json", "w", encoding="utf-8") as f:
    json.dump(unique_keys, f, indent=2)
