import os
from playwright.sync_api import sync_playwright
import time

IMG_DIR = '/Volumes/Samsung X5/Blogs/tistory-blog/trend-tistory/images/2026-07-10-monsoon-season'
os.makedirs(IMG_DIR, exist_ok=True)
profile_dir = os.path.abspath('temp_playwright_profile')

html_templates = {
    'info1_summary.html': '''
    <body style="font-family:'Malgun Gothic',sans-serif; margin:0; padding:40px; background:linear-gradient(135deg, #1e3c72, #2a5298); color:white; width:800px; height:600px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; box-sizing:border-box;">
        <h1 style="font-size:48px; margin-bottom:20px; text-shadow:2px 2px 4px rgba(0,0,0,0.3);">2026년 장마기간 핵심 요약</h1>
        <div style="background:rgba(255,255,255,0.1); padding:30px; border-radius:15px; width:90%; border:2px solid rgba(255,255,255,0.2);">
            <h2 style="font-size:32px; color:#ffd700; margin-top:0;">⚡ 평년보다 늦은 '지각 장마'</h2>
            <p style="font-size:24px; line-height:1.6; margin:10px 0;">✔ 남부·제주: 6월 30일 시작<br/>✔ 중부지방: 7월 1일 시작<br/>✔ 종료 예상: 7월 말 (변동 가능)</p>
            <p style="font-size:20px; margin-top:20px; font-weight:bold; color:#ffdddd;">*기습적 국지성 폭우 및 야행성 폭우 주의</p>
        </div>
    </body>
    ''',
    'info2_dates.html': '''
    <body style="font-family:'Malgun Gothic',sans-serif; margin:0; padding:40px; background:#f4f7f6; color:#333; width:800px; height:600px; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing:border-box;">
        <h1 style="font-size:48px; color:#2c3e50; margin-bottom:40px;">📍 2026년 지역별 장마 시작일 비교</h1>
        <table style="width:100%; border-collapse:collapse; text-align:center; font-size:28px; background:white; border-radius:15px; overflow:hidden; box-shadow:0 10px 20px rgba(0,0,0,0.05);">
            <tr style="background:#34495e; color:white;">
                <th style="padding:20px;">지역</th>
                <th style="padding:20px;">평년 시작일</th>
                <th style="padding:20px;">2026년 시작일</th>
            </tr>
            <tr>
                <td style="padding:20px; border-bottom:1px solid #ddd;">제주도</td>
                <td style="padding:20px; border-bottom:1px solid #ddd;">6월 19일</td>
                <td style="padding:20px; border-bottom:1px solid #ddd; font-weight:bold; color:#e74c3c;">6월 30일 (11일 지연)</td>
            </tr>
            <tr>
                <td style="padding:20px; border-bottom:1px solid #ddd;">남부지방</td>
                <td style="padding:20px; border-bottom:1px solid #ddd;">6월 23일</td>
                <td style="padding:20px; border-bottom:1px solid #ddd; font-weight:bold; color:#e74c3c;">6월 30일 (7일 지연)</td>
            </tr>
            <tr>
                <td style="padding:20px;">중부지방</td>
                <td style="padding:20px;">6월 25일</td>
                <td style="padding:20px; font-weight:bold; color:#e74c3c;">7월 1일 (6일 지연)</td>
            </tr>
        </table>
    </body>
    ''',
    'info3_cause.html': '''
    <body style="font-family:'Malgun Gothic',sans-serif; margin:0; padding:40px; background:#e0f7fa; color:#006064; width:800px; height:600px; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing:border-box;">
        <h1 style="font-size:46px; margin-bottom:30px;">🤔 올해 장마는 왜 늦어졌을까?</h1>
        <div style="display:flex; justify-content:space-around; width:100%; gap:20px;">
            <div style="background:white; padding:30px; border-radius:20px; width:45%; box-shadow:0 8px 15px rgba(0,0,0,0.1); text-align:center;">
                <h2 style="font-size:30px; color:#00838f;">블로킹 현상</h2>
                <p style="font-size:22px; line-height:1.5;">한반도 상공에 찬 공기가 정체하며 북태평양 고기압의 북상을 저지함</p>
            </div>
            <div style="background:white; padding:30px; border-radius:20px; width:45%; box-shadow:0 8px 15px rgba(0,0,0,0.1); text-align:center;">
                <h2 style="font-size:30px; color:#00838f;">해수면 온도 변화</h2>
                <p style="font-size:22px; line-height:1.5;">엘니뇨에서 라니냐로 전환되는 과정의 기후 변동성 증대</p>
            </div>
        </div>
    </body>
    ''',
    'info4_features.html': '''
    <body style="font-family:'Malgun Gothic',sans-serif; margin:0; padding:40px; background:#fff3e0; color:#e65100; width:800px; height:600px; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing:border-box;">
        <h1 style="font-size:48px; margin-bottom:30px;">🚨 2026년 장마 3대 위험 요소</h1>
        <div style="width:100%; display:flex; flex-direction:column; gap:20px;">
            <div style="background:white; padding:20px 40px; border-radius:15px; border-left:10px solid #ff9800; font-size:24px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <b>1. 야행성 기습 폭우</b> : 취약 시간대인 밤~새벽 사이 집중호우 빈발
            </div>
            <div style="background:white; padding:20px 40px; border-radius:15px; border-left:10px solid #ff5722; font-size:24px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <b>2. 국지성 물폭탄</b> : 좁은 지역에 짧은 시간 동안 쏟아지는 극단적 강수
            </div>
            <div style="background:white; padding:20px 40px; border-radius:15px; border-left:10px solid #f44336; font-size:24px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <b>3. 찜통더위(마른 장마)</b> : 비가 오지 않을 때는 습도가 높은 폭염·열대야 기승
            </div>
        </div>
    </body>
    ''',
    'info5_checklist.html': '''
    <body style="font-family:'Malgun Gothic',sans-serif; margin:0; padding:40px; background:#e8f5e9; color:#1b5e20; width:800px; height:600px; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing:border-box;">
        <h1 style="font-size:48px; margin-bottom:20px;">📝 장마철 필수 대비 체크리스트</h1>
        <ul style="list-style-type:none; padding:0; margin:0; width:90%;">
            <li style="background:white; padding:20px; margin-bottom:15px; border-radius:10px; font-size:26px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">✅ <b>배수로 점검</b> : 집 주변, 베란다 배수구 막힘 확인</li>
            <li style="background:white; padding:20px; margin-bottom:15px; border-radius:10px; font-size:26px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">✅ <b>실내 제습</b> : 제습기 가동 및 제습제 비치로 곰팡이 방지</li>
            <li style="background:white; padding:20px; margin-bottom:15px; border-radius:10px; font-size:26px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">✅ <b>위생 관리</b> : 식중독 예방을 위한 철저한 식자재 보관</li>
            <li style="background:white; padding:20px; border-radius:10px; font-size:26px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">✅ <b>기상 확인</b> : 기상청 실시간 레이더 앱 설치 및 알림 설정</li>
        </ul>
    </body>
    '''
}

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        channel='chrome',
        args=['--disable-blink-features=AutomationControlled'],
        viewport={'width': 800, 'height': 600}
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    for filename, content in html_templates.items():
        html_path = os.path.abspath(filename)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        page.goto(f'file://{html_path}')
        time.sleep(1)
        page.screenshot(path=f'{IMG_DIR}/{filename.replace(".html", ".png")}')
        os.remove(html_path)
        
    try:
        page.goto('https://www.weather.go.kr/w/index.do', timeout=30000)
        time.sleep(4)
        page.screenshot(path=f'{IMG_DIR}/kma_main.png')
    except Exception as e:
        print(f"Failed KMA main: {e}")
        
    try:
        page.goto('https://www.weather.go.kr/w/image/vshm.do', timeout=30000)
        time.sleep(4)
        page.screenshot(path=f'{IMG_DIR}/kma_satellite.png')
    except Exception as e:
        print(f"Failed KMA satellite: {e}")

    context.close()
