import os
import sys
import time
import requests
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
url = "https://www.google.com/maps/place/Ella+Estetik+Ve+G%C3%BCzellik/@36.8703419,30.6281994,17z/data=!3m1!4b1!4m6!3m5!1s0x14c391652edb708b:0x9d1f75a00a75b3c7!8m2!3d36.8703419!4d30.6281994!16s%2Fg%2F11s3jxx422?entry=ttu&g_ep=EgoyMDI2MTEwNC4wIKXMDSoASAFQAw%3D%3D"

video_downloaded = False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        locale="tr-TR",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    def handle_request(req):
        global video_downloaded
        if video_downloaded:
            return
        if "videoplayback" in req.url:
            print("Detected videoplayback request!")
            req_headers = req.headers
            try:
                # Use requests to download using same headers
                r = requests.get(req.url, headers=req_headers, stream=True, timeout=20)
                print(f"Fetch videoplayback response: {r.status_code}")
                if r.status_code in [200, 206]:
                    with open("assets/videos/cilt-bakimi-uygulama.mp4", "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024*64):
                            if chunk:
                                f.write(chunk)
                    size = os.path.getsize("assets/videos/cilt-bakimi-uygulama.mp4")
                    print(f"SUCCESS: Saved assets/videos/cilt-bakimi-uygulama.mp4 ({size} bytes)!")
                    video_downloaded = True
            except Exception as e:
                print("Error fetching video directly:", e)

    page.on("request", handle_request)

    print("Opening Maps...")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    photo_btn = page.locator("button[aria-label*='fotoğraf' i], button[aria-label*='Fotoğraflar' i]").first
    if not photo_btn.is_visible():
        photo_btn = page.locator("text='Fotoğraflar'").first
    photo_btn.click()
    time.sleep(3)

    items = page.locator("div.m6QErb a, div.m6QErb div[role='img']").all()
    if len(items) > 1:
        print("Clicking video thumbnail...")
        items[1].click()
        time.sleep(5)

    browser.close()

if os.path.exists("assets/videos/cilt-bakimi-uygulama.mp4"):
    print("Final video size:", os.path.getsize("assets/videos/cilt-bakimi-uygulama.mp4"))
