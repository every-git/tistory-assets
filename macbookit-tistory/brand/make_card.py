#!/usr/bin/env python3
"""맥부킷 카드 썸네일 생성 — 세로형 1080×1350.

🚨 목록이 세로로 크롭한다. 가로형(1536×1024)을 쓰면 좌우가 잘려 글자가 반토막 난다
   (2026-08-28 실측 — 기존 글들도 같은 증상이었다).
🚨 여백을 넉넉히 두면 목록에서 «빈 카드»로 보인다. 위아래를 꽉 채운다.

  python3 make_card.py --slug ghostty-... --kicker "Ghostty" \
     --title "공식이|「찾으세요」|라고만 한" --sub "설정 파일 위치와|한글 폰트 문제"
  (제목·부제의 | 는 줄바꿈)
"""
import argparse, subprocess, tempfile
from pathlib import Path

BRAND = Path(__file__).parent
CARDS = BRAND.parent / "images" / "cards"
WEBSHOT = Path.home() / ".claude/skills/webshot/bin/webshot"

TPL = """<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="{css}">
<div class="top">{kicker}</div>
<div class="mid"><h1>{title}</h1><div class="rule"></div><div class="sub">{sub}</div></div>
<div class="bot"><span>맥부킷</span><span>{date}</span></div>
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--kicker", required=True, help="상단 라벨 (예: Ghostty)")
    ap.add_argument("--title", required=True, help="큰 제목. | 로 줄바꿈")
    ap.add_argument("--sub", required=True, help="부제. | 로 줄바꿈")
    ap.add_argument("--date", default="2026-08")
    a = ap.parse_args()

    html = TPL.format(css=BRAND / "card-vertical.css", kicker=a.kicker,
                      title=a.title.replace("|", "<br>"),
                      sub=a.sub.replace("|", "<br>"), date=a.date)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html); tmp = f.name
    png = Path(tmp).with_suffix(".png")
    subprocess.run([str(WEBSHOT), "--url", f"file://{tmp}", "--output", str(png),
                    "--width", "1080", "--height", "1350", "--dpr", "1", "--wait", "600"], check=True)
    CARDS.mkdir(parents=True, exist_ok=True)
    out = CARDS / f"{a.slug}.jpg"
    from PIL import Image
    Image.open(png).convert("RGB").save(out, "JPEG", quality=92)
    print(f"✓ {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
