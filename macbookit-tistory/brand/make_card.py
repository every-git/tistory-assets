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
from pathlib import Path as pathlib_Path

BRAND = Path(__file__).parent
CARDS = BRAND.parent / "images" / "cards"   # 기본: 맥부킷
WEBSHOT = Path.home() / ".claude/skills/webshot/bin/webshot"

# 카테고리별 색 — cupertino-design.md §2. 레이아웃은 공유하고 변수만 갈아끼운다.
PALETTES = {
    "clay": "",   # 기본값(CSS :root)을 그대로 쓴다 — Claude code
    "blue": (":root{--bg:#F5F5F7;--kicker:#0066CC;--rule:#0071E3;"
             "--title:#1D1D1F;--sub:#6E6E73;--hair:#D2D2D7;--foot:#6E6E73}"),
    # 도와줘요 경자씨 — 경자 그린 + 종이 크림(kyungja 프로필 paper #F2F1ED)
    "green": (":root{--bg:#F2F1ED;--kicker:#1E6E46;--rule:#1E6E46;"
              "--title:#1A1A1A;--sub:#4A4A48;--hair:#DFDCD3;--foot:#8C887F}"),
}

TPL = """<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="{css}">
<style>{palette}</style>
<div class="top">{kicker}</div>
<div class="mid"><h1>{title}</h1><div class="rule"></div><div class="sub">{sub}</div></div>
<div class="bot"><span>{brand}</span><span>{date}</span></div>
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--kicker", required=True, help="상단 라벨 (예: Ghostty)")
    ap.add_argument("--title", required=True, help="큰 제목. | 로 줄바꿈")
    ap.add_argument("--sub", required=True, help="부제. | 로 줄바꿈")
    ap.add_argument("--date", default="2026-08")
    ap.add_argument("--brand", default="맥부킷", help="카드 하단 브랜드명")
    ap.add_argument("--out-dir", help="카드를 쓸 디렉터리(기본: 맥부킷 images/cards)")
    ap.add_argument("--palette", choices=sorted(PALETTES), default="clay",
                    help="clay=Claude code · blue=Apple & Mac · green=도와줘요 경자씨")
    a = ap.parse_args()

    pal = PALETTES[a.palette]
    html = TPL.format(css=BRAND / "card-vertical.css", palette=pal,
                      kicker=a.kicker,
                      title=a.title.replace("|", "<br>"),
                      sub=a.sub.replace("|", "<br>"), date=a.date, brand=a.brand)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html); tmp = f.name
    png = Path(tmp).with_suffix(".png")
    subprocess.run([str(WEBSHOT), "--url", f"file://{tmp}", "--output", str(png),
                    "--width", "1080", "--height", "1350", "--dpr", "1", "--wait", "600"], check=True)
    cards = pathlib_Path(a.out_dir) if a.out_dir else CARDS
    cards.mkdir(parents=True, exist_ok=True)
    out = cards / f"{a.slug}.jpg"
    from PIL import Image
    Image.open(png).convert("RGB").save(out, "JPEG", quality=92)
    print(f"✓ {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
