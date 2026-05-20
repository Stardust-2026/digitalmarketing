"""Render LinkedIn carousel HTML slides → screenshots + PDF."""
from playwright.sync_api import sync_playwright
import os

HTML_PATH = "/home/josh/Development/Projects/digitalmarketing/prototypes/carousel-template.html"
OUTPUT_DIR = "/home/josh/Development/Projects/digitalmarketing/prototypes"
PDF_PATH = os.path.join(OUTPUT_DIR, "carousel-how-to-outmaneuver-competitors.pdf")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1080})
    page.goto(f"file://{HTML_PATH}")
    page.wait_for_timeout(1000)

    slides = page.locator(".slide")
    count = slides.count()
    print(f"Found {count} slides")

    screenshot_paths = []
    for i in range(count):
        path = os.path.join(OUTPUT_DIR, f"slide_{i+1:02d}.png")
        slides.nth(i).screenshot(path=path)
        screenshot_paths.append(path)
        print(f"  Slide {i+1}/{count} → {os.path.basename(path)}")

    browser.close()

    # Convert to PDF using Pillow
    from PIL import Image
    images = [Image.open(p).convert("RGB") for p in screenshot_paths]
    images[0].save(PDF_PATH, save_all=True, append_images=images[1:], quality=95)
    print(f"\n✅ PDF created: {PDF_PATH}")
    print(f"   {count} slides, {os.path.getsize(PDF_PATH)//1024} KB")
