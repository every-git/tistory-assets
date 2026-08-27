from playwright.sync_api import sync_playwright
import time
import os

IMG_DIR = '/Volumes/Samsung X5/Blogs/tistory-blog/trend-tistory/images/2026-07-10-monsoon-season'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 800})
    
    print("Fetching forecast...")
    page.goto('https://www.weather.go.kr/w/weather/forecast/short-term.do')
    time.sleep(3)
    page.screenshot(path=f'{IMG_DIR}/kma_forecast.png')
    
    print("Fetching satellite...")
    page.goto('https://www.weather.go.kr/w/image/sat/gk2a.do')
    time.sleep(4)
    page.screenshot(path=f'{IMG_DIR}/kma_sat.png')
    
    browser.close()
    print("Done")
