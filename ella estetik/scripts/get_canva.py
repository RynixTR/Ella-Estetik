import requests
from playwright.sync_api import sync_playwright

url = "https://ellaestetik.my.canva.site"
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            locale="tr-TR",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(3000)
        
        print("Canva Site Title:", page.title())
        text = page.locator("body").inner_text()
        with open("canva_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Canva text saved ({len(text)} chars)")
        page.screenshot(path="canva_screenshot.png")
        browser.close()
except Exception as e:
    print("Canva fetch error:", e)
