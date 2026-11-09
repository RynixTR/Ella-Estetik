import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

url = "https://www.google.com/maps/place/Ella+Estetik+Ve+G%C3%BCzellik/@36.8703419,30.6281994,17z/data=!3m1!4b1!4m6!3m5!1s0x14c391652edb708b:0x9d1f75a00a75b3c7!8m2!3d36.8703419!4d30.6281994!16s%2Fg%2F11s3jxx422?entry=ttu&g_ep=EgoyMDI2MTEwNC4wIKXMDSoASAFQAw%3D%3D"

print("Starting playwright...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        locale="tr-TR",
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    print("Navigating to URL with domcontentloaded...", flush=True)
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print(f"Goto error: {e}", flush=True)

    print("Page loaded, sleeping 5s to allow rendering...", flush=True)
    time.sleep(5)
    
    current_url = page.url
    title = page.title()
    content = page.content()
    print(f"Current URL: {current_url}", flush=True)
    print(f"Page Title: {title}", flush=True)
    
    # Check for captcha or blocking
    if "unusual traffic" in content.lower() or "captcha" in content.lower() or "robot" in title.lower():
        print("BLOCKED_DETECTED: Captcha or unusual traffic detected.", flush=True)
        page.screenshot(path="captcha_detected.png")
        browser.close()
        sys.exit(2)

    # Check for consent buttons
    buttons = page.locator("button").all()
    for btn in buttons:
        try:
            txt = btn.inner_text().strip()
            if any(c in txt for c in ["Tümünü kabul et", "Kabul et", "Accept all", "Hepsini kabul et"]):
                print(f"Found consent button: '{txt}', clicking...", flush=True)
                btn.click()
                time.sleep(4)
                break
        except Exception:
            pass

    page.screenshot(path="page_screenshot.png")
    print("Screenshot saved to page_screenshot.png", flush=True)
    print("Page title now:", page.title(), flush=True)

    # Let's write the text content of the page to inspect
    text = page.locator("body").inner_text()
    with open("page_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote page_text.txt ({len(text)} characters)", flush=True)

    browser.close()
    print("Done!", flush=True)
