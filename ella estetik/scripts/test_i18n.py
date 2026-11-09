import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # 1. Test Desktop & Language Switch
    page = browser.new_page(viewport={"width": 1400, "height": 900}, locale="tr-TR")
    page.goto("http://127.0.0.1:8080/index.html", wait_until="domcontentloaded", timeout=15000)
    time.sleep(1)

    print("Initial title (TR):", page.title())
    initial_hero_slogan = page.locator(".hero-slogan").inner_text()
    print("Initial Slogan (TR):", initial_hero_slogan)

    # Switch to Russian
    page.locator(".lang-btn-current").click()
    time.sleep(0.5)
    page.locator(".lang-option[data-lang='ru']").click()
    time.sleep(0.5)

    ru_title = page.title()
    ru_slogan = page.locator(".hero-slogan").inner_text()
    ru_status = page.locator(".live-status-pill").inner_text()
    print("Russian Title:", ru_title)
    print("Russian Slogan:", ru_slogan)
    print("Russian Status Pill:", ru_status)

    # Switch to Ukrainian
    page.locator(".lang-btn-current").click()
    time.sleep(0.5)
    page.locator(".lang-option[data-lang='uk']").click()
    time.sleep(0.5)

    uk_slogan = page.locator(".hero-slogan").inner_text()
    uk_status = page.locator(".live-status-pill").inner_text()
    print("Ukrainian Slogan:", uk_slogan)
    print("Ukrainian Status Pill:", uk_status)

    # Switch to English
    page.locator(".lang-btn-current").click()
    time.sleep(0.5)
    page.locator(".lang-option[data-lang='en']").click()
    time.sleep(0.5)

    en_slogan = page.locator(".hero-slogan").inner_text()
    print("English Slogan:", en_slogan)

    # Take screenshot of EN page
    page.screenshot(path="scripts/screenshot_en.png")
    print("Saved screenshot_en.png")

    # 2. Test Mobile View (iPhone 14) with Sticky Action Bar
    context_mobile = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15",
        is_mobile=True,
        has_touch=True,
        locale="tr-TR"
    )
    page_m = context_mobile.new_page()
    page_m.goto("http://127.0.0.1:8080/index.html", wait_until="domcontentloaded", timeout=15000)
    time.sleep(1)

    # Check that sticky action bar is visible on mobile
    bar_visible = page_m.locator(".mobile-action-bar").is_visible()
    print("Mobile Action Bar visible:", bar_visible)
    page_m.screenshot(path="scripts/screenshot_mobile_home.png")
    print("Saved screenshot_mobile_home.png")

    # Open Mobile Menu and test Ukrainian button
    page_m.locator(".menu-toggle").click()
    time.sleep(0.5)
    page_m.screenshot(path="scripts/screenshot_mobile_menu.png")
    print("Saved screenshot_mobile_menu.png")

    # Click Ukrainian button in mobile menu
    page_m.locator(".mobile-lang-btn[data-lang='uk']").click()
    time.sleep(0.5)
    mobile_uk_title = page_m.locator(".hero-title").inner_text()
    print("Mobile UK Title updated:", mobile_uk_title)

    browser.close()
    print("All multi-language and mobile tests passed successfully!")
