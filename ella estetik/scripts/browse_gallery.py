import os
import sys
import time
import json
import urllib.request
from PIL import Image
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

    # Click on the hero/main photo button
    photo_btn = page.locator("button[aria-label*='fotoğraf' i], button[aria-label*='Fotoğraflar' i]").first
    if not photo_btn.is_visible():
        photo_btn = page.locator("text='Fotoğraflar'").first
    photo_btn.click()
    time.sleep(3)

    # Now click the first photo in the gallery
    first_photo = page.locator("a[data-photo-index='0'], div.m6QErb a[href*='photo']").first
    if first_photo.is_visible():
        first_photo.click()
    else:
        # Click by position or image
        page.mouse.click(400, 200)
    time.sleep(3)

    photos_data = []
    print("Navigating through photo viewer...")
    for i in range(25):
        # Read uploader / caption
        try:
            uploader_el = page.locator("div.fontHeadlineSmall, div.fontTitleLarge, a[aria-label*='fotoğraf' i]").all()
            texts = [el.inner_text().strip() for el in uploader_el if el.inner_text().strip()]
            
            # Find image src on main display
            img_el = page.locator("div[role='region'] img, div[aria-label*='Fotoğraf' i] img").first
            src = img_el.get_attribute("src") if img_el.is_visible() else None
            
            print(f"Photo {i}: src={src[:80] if src else 'None'} | texts={texts[:3]}")
            if src:
                photos_data.append({"index": i, "src": src, "meta": texts})
        except Exception as e:
            print(f"Error reading photo {i}:", e)

        # Press ArrowRight
        page.keyboard.press("ArrowRight")
        time.sleep(1)

    with open("gallery_extracted.json", "w", encoding="utf-8") as f:
        json.dump(photos_data, f, ensure_ascii=False, indent=2)

    browser.close()
