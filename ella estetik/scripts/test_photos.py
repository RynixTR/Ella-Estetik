import os
import time
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

    # Click on the main photo / "Fotoğrafları göster" or photo gallery button
    try:
        # Find photo button
        photo_btn = page.locator("button[aria-label*='fotoğraf' i], button[aria-label*='Fotoğraflar' i]").first
        if not photo_btn.is_visible():
            photo_btn = page.locator("text='Fotoğraflar'").first
        
        print("Clicking photo button...", flush=True)
        photo_btn.click()
        time.sleep(4)
        page.screenshot(path="photos_tab.png")
        print("Screenshot saved to photos_tab.png", flush=True)

        # Check tabs inside photos (e.g. "Tümü", "Sahibi tarafından", "İç mekan", "Videolar" etc.)
        tabs = page.locator("button[role='tab']").all()
        tab_names = [t.inner_text() for t in tabs]
        print("Photo tabs found:", tab_names, flush=True)

        # Look for "Sahibi tarafından" or "İşletme sahibi" tab
        for tab in tabs:
            txt = tab.inner_text().lower()
            if "sahibi" in txt or "iç mekan" in txt or "hizmetler" in txt:
                print(f"Clicking tab: {tab.inner_text()}", flush=True)
                tab.click()
                time.sleep(3)
                break
                
        # Find image elements
        img_elements = page.locator("div[role='img'], a[data-photo-index]").all()
        print(f"Found {len(img_elements)} photo containers/elements", flush=True)
        
    except Exception as e:
        print("Photo click error:", e, flush=True)

    browser.close()
