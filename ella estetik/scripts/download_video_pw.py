import os
import time
from playwright.sync_api import sync_playwright

url = "https://www.google.com/maps/place/Ella+Estetik+Ve+G%C3%BCzellik/@36.8703419,30.6281994,17z/data=!3m1!4b1!4m6!3m5!1s0x14c391652edb708b:0x9d1f75a00a75b3c7!8m2!3d36.8703419!4d30.6281994!16s%2Fg%2F11s3jxx422?entry=ttu&g_ep=EgoyMDI2MTEwNC4wIKXMDSoASAFQAw%3D%3D"

os.makedirs("assets/videos", exist_ok=True)
downloaded_video = False

def run():
    global downloaded_video
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="tr-TR",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def on_response(response):
            global downloaded_video
            res_url = response.url
            content_type = response.headers.get("content-type", "")
            if "video/mp4" in content_type and not downloaded_video:
                try:
                    body = response.body()
                    if len(body) > 100000:
                        filename = "assets/videos/cilt-bakimi-uygulama.mp4"
                        with open(filename, "wb") as f:
                            f.write(body)
                        print(f"Successfully saved {filename} ({len(body)} bytes)!")
                        downloaded_video = True
                except Exception as e:
                    print("Error saving video body:", e)

        page.on("response", on_response)

        print("Navigating to Google Maps...")
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
            time.sleep(8)

        browser.close()

run()
if os.path.exists("assets/videos/cilt-bakimi-uygulama.mp4"):
    print("Video downloaded successfully, size:", os.path.getsize("assets/videos/cilt-bakimi-uygulama.mp4"))
else:
    print("No video saved.")
