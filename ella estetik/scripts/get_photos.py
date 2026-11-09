import os
import re
import json
import time
import requests
from playwright.sync_api import sync_playwright

url = "https://www.google.com/maps/place/Ella+Estetik+Ve+G%C3%BCzellik/@36.8703419,30.6281994,17z/data=!3m1!4b1!4m6!3m5!1s0x14c391652edb708b:0x9d1f75a00a75b3c7!8m2!3d36.8703419!4d30.6281994!16s%2Fg%2F11s3jxx422?entry=ttu&g_ep=EgoyMDI2MTEwNC4wIKXMDSoASAFQAw%3D%3D"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        locale="tr-TR",
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(4)

    # Click photo button
    try:
        photo_btn = page.locator("button[aria-label*='fotoğraf' i], button[aria-label*='Fotoğraflar' i]").first
        if not photo_btn.is_visible():
            photo_btn = page.locator("text='Fotoğraflar'").first
        photo_btn.click()
        time.sleep(3)
    except Exception as e:
        print("Click error:", e)

    # Look for category chips like "Tümü", "Sahibi tarafından", etc.
    chips = page.locator("button[role='radio'], div[role='tablist'] button, div.m6QErb button").all()
    print("Found chips:", [c.inner_text() for c in chips if c.inner_text().strip()])

    # Try scrolling down the photo list to load more photos
    scrollable = page.locator("div.m6QErb.D98jfm").first
    for _ in range(5):
        page.keyboard.press("PageDown")
        time.sleep(1)

    html = page.content()
    with open("photos_html.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved photos_html.html")

    # Find all googleusercontent URLs
    matches = re.findall(r'https:\/\/[a-z0-9\.\-]+\.googleusercontent\.com\/p\/[A-Za-z0-9_\-]+', html)
    unique_ids = list(dict.fromkeys(matches))
    print(f"Found {len(unique_ids)} unique photo base URLs:")
    for uid in unique_ids[:15]:
        print(" -", uid)

    browser.close()
