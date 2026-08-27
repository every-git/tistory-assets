from playwright.sync_api import sync_playwright
import time
import os

profile_dir = os.path.abspath('temp_playwright_profile')

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        channel='chrome',
        args=['--disable-blink-features=AutomationControlled']
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto('https://www.tomsguide.com/news/iphone-flip', timeout=60000)
    time.sleep(5)
    
    images = page.locator('img').all()
    count = 5
    for img in images:
        try:
            box = img.bounding_box()
            if box and box['width'] > 300 and box['height'] > 200:
                img.scroll_into_view_if_needed()
                time.sleep(0.5)
                img.screenshot(path=f'images/2026-07-10-iphone-fold/rumor_photo_{count}.jpg', type='jpeg')
                count += 1
                if count > 6:
                    break
        except Exception as e:
            pass
    context.close()
