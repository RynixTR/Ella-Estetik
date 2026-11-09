import os
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Desktop Test
    context_desktop = browser.new_context(
        viewport={"width": 1440, "height": 900},
        locale="tr-TR"
    )
    page_d = context_desktop.new_page()
    page_d.goto("http://127.0.0.1:8080/index.html", wait_until="domcontentloaded", timeout=15000)
    time.sleep(1)
    
    # Scroll through to trigger any intersection observers
    for _ in range(8):
        page_d.mouse.wheel(0, 1000)
        time.sleep(0.2)
    page_d.mouse.wheel(0, -10000)
    time.sleep(1)

    page_d.screenshot(path="desktop_preview.png", full_page=True)
    print("Saved desktop_preview.png")

    # 2. Mobile Test (iPhone 14)
    context_mobile = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        is_mobile=True,
        has_touch=True,
        locale="tr-TR"
    )
    page_m = context_mobile.new_page()
    page_m.goto("http://127.0.0.1:8080/index.html", wait_until="domcontentloaded", timeout=15000)
    time.sleep(1)
    for _ in range(8):
        page_m.mouse.wheel(0, 1000)
        time.sleep(0.2)
    page_m.mouse.wheel(0, -10000)
    time.sleep(1)

    page_m.screenshot(path="mobile_preview.png", full_page=True)
    print("Saved mobile_preview.png")

    browser.close()
