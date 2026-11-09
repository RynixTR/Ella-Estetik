import json
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

    # Click on hours dropdown if exists
    try:
        # Looking for the button containing "Açılış zamanı" or aria-label for hours
        hours_btn = page.locator("[data-item-id='oh']").first
        if hours_btn.is_visible():
            hours_btn.click()
            time.sleep(1)
        else:
            # Try clicking near "Kapalı"
            page.locator("text=Açılış zamanı").first.click()
            time.sleep(1)
    except Exception as e:
        print("Hours click exception:", e)

    # Get hours table text
    hours_info = []
    try:
        tables = page.locator("table").all()
        for t in tables:
            hours_info.append(t.inner_text())
    except Exception as e:
        print("Table extract exception:", e)
    
    print("Hours info:", hours_info)
    with open("hours.json", "w", encoding="utf-8") as f:
        json.dump(hours_info, f, ensure_ascii=False, indent=2)

    browser.close()
