import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.google.com/maps/place/Ella+Estetik+Ve+G%C3%BCzellik/@36.8703419,30.6281994,17z/data=!3m1!4b1!4m6!3m5!1s0x14c391652edb708b:0x9d1f75a00a75b3c7!8m2!3d36.8703419!4d30.6281994!16s%2Fg%2F11s3jxx422?entry=ttu&g_ep=EgoyMDI2MTEwNC4wIKXMDSoASAFQAw%3D%3D"

video_urls = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        locale="tr-TR",
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    def handle_response(response):
        res_url = response.url
        content_type = response.headers.get("content-type", "")
        if "video" in content_type or ".mp4" in res_url or "googlevideo.com" in res_url:
            print(f"Captured Video URL: {res_url} (Type: {content_type})")
            video_urls.append(res_url)

    page.on("response", handle_response)

    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # Click photo gallery
    photo_btn = page.locator("button[aria-label*='fotoğraf' i], button[aria-label*='Fotoğraflar' i]").first
    if not photo_btn.is_visible():
        photo_btn = page.locator("text='Fotoğraflar'").first
    photo_btn.click()
    time.sleep(3)

    # Now click on the 2nd thumbnail (which has the 0:18 video!)
    # On the left pane, let's click around x=200, y=250 or locate the thumbnail
    print("Clicking the video thumbnail...")
    # Find all clickable photo items in left list
    items = page.locator("div.m6QErb a, div.m6QErb div[role='img']").all()
    print(f"Found {len(items)} photo gallery items")
    if len(items) > 1:
        items[1].click()
    else:
        page.mouse.click(220, 240)
    
    time.sleep(5)

    # Check for video tag
    videos = page.locator("video").all()
    print(f"Video elements on page: {len(videos)}")
    for v in videos:
        src = v.get_attribute("src")
        print(f"Video src: {src}")
        if src:
            video_urls.append(src)

    # Click next photo arrow a few times to load more
    next_btn = page.locator("button[aria-label*='Sonraki' i], button[aria-label*='Next' i]").first
    for step in range(12):
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(1.5)
        else:
            page.keyboard.press("ArrowRight")
            time.sleep(1.5)

    browser.close()

with open("captured_videos.json", "w", encoding="utf-8") as f:
    json.dump(video_urls, f, indent=2)
print("Finished! Captured video urls:", len(video_urls))
