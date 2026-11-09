import re
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://ellaestetik.my.canva.site", wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(3000)
    
    # Extract all img elements and background-image styles
    imgs = page.locator("img").all()
    print("Img count on Canva:", len(imgs))
    for i, img in enumerate(imgs):
        src = img.get_attribute("src")
        print(f"Img {i}: {src}")
        
    html = page.content()
    with open("canva_html.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    browser.close()
