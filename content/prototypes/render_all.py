"""Render all 3 carousel parts into slides + PDFs."""
from playwright.sync_api import sync_playwright
import os
from PIL import Image

PARTS = [
    ("part1-strategy.html", "carousel-part1-strategy"),
    ("part2-framework.html", "carousel-part2-framework"),
    ("part3-action.html", "carousel-part3-action"),
]

OUTPUT_DIR = "/home/josh/Development/Projects/digitalmarketing/prototypes"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    for html_file, pdf_name in PARTS:
        html_path = os.path.join(OUTPUT_DIR, html_file)
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(1000)
        
        slides = page.locator(".slide")
        count = slides.count()
        print(f"\n{html_file}: {count} slides")
        
        screenshot_paths = []
        for i in range(count):
            path = os.path.join(OUTPUT_DIR, f"{pdf_name}_slide_{i+1:02d}.png")
            slides.nth(i).screenshot(path=path)
            screenshot_paths.append(path)
            print(f"  Slide {i+1}/{count} → {os.path.basename(path)}")
        
        # Create PDF (skip if JPEG not available)
        try:
            pdf_path = os.path.join(OUTPUT_DIR, f"{pdf_name}.pdf")
            images = [Image.open(p).convert("RGB") for p in screenshot_paths]
            images[0].save(pdf_path, save_all=True, append_images=images[1:], quality=95)
            print(f"  PDF → {os.path.basename(pdf_path)} ({os.path.getsize(pdf_path)//1024} KB)")
        except Exception as e:
            print(f"  PDF skipped ({e})")
        
        page.close()
    
    browser.close()
    print("\n✅ All 3 parts rendered!")
