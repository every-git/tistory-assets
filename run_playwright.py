from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('images/2026-07-10-iphone-fold', exist_ok=True)
profile_dir = os.path.abspath('temp_playwright_profile')

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        channel='chrome',
        args=['--disable-blink-features=AutomationControlled']
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto('https://www.macrumors.com/roundup/foldable-iphone/', timeout=60000)
    time.sleep(5)
    
    # take screenshots of the first 6 large images in the article
    images = page.locator('img').all()
    count = 1
    for img in images:
        try:
            box = img.bounding_box()
            if box and box['width'] > 250 and box['height'] > 150:
                img.scroll_into_view_if_needed()
                time.sleep(0.5)
                img.screenshot(path=f'images/2026-07-10-iphone-fold/rumor_photo_{count}.jpg', type='jpeg')
                count += 1
                if count > 6:
                    break
        except Exception as e:
            pass
    context.close()
