#!/usr/bin/env python3
"""계열 공통 상단 배너 — 네이버 dokyungja·doonablog 문법(1400×400).

라벨 뱃지 → 헤드라인 2줄 → 부제 → 우측 원형 심볼 → 굵은 하단선.
네이버 두 블로그가 이 문법을 공유한다. 티스토리에도 같은 문법을 쓰면
어느 채널을 봐도 «같은 집»으로 읽힌다.

  python3 make_banner.py --badge "Mac · Claude" \
     --title "맥북과 클로드,|막힌 데만 짚어 드립니다" \
     --sub "설정 · 단축키 · 카플레이 · 클로드 코드 — *맥부킷*" \
     --out banner-macbookit.png
  (제목의 | 는 줄바꿈 · 부제의 *…* 는 브랜드색 강조)
"""
import argparse, subprocess, tempfile
from pathlib import Path

BRAND = Path(__file__).parent
WEBSHOT = Path.home() / ".claude/skills/webshot/bin/webshot"

# 색만 갈아끼운다 — 레이아웃은 계열 공통이다
PALETTES = {
    "blue": "",  # 기본값(banner.css :root)
    "clay": (":root{--bg1:#F5F1E8;--bg2:#FAF9F5;--badge-bg:#F3EADA;--badge:#A8452A;"
             "--head:#191919;--sub:#6B6862;--brand:#A8452A;--rule:#191919}"),
    "green": (":root{--bg1:#EDF4EE;--bg2:#FFFFFF;--badge-bg:#DCEBDF;--badge:#1E6E46;"
              "--head:#1A1A1A;--sub:#6B6862;--brand:#1E6E46;--rule:#1A1A1A}"),
}

TPL = """<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="{css}">
<style>{palette}</style>
<div>
  <span class="badge">{badge}</span>
  <h1>{title}</h1>
  <div class="sub">{sub}</div>
</div>
{mark}
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--badge", required=True, help="라벨 뱃지 (예: Mac · Claude)")
    ap.add_argument("--title", required=True, help="헤드라인. | 로 줄바꿈")
    ap.add_argument("--sub", required=True, help="부제. *…* 는 브랜드색")
    ap.add_argument("--mark", default="profile-circle.png",
                    help="우측 원형 심볼 파일명 (brand/ 기준). 'none' 이면 뺀다")
    ap.add_argument("--palette", choices=sorted(PALETTES), default="blue")
    ap.add_argument("--out", required=True, help="결과 png 경로 (brand/ 기준 가능)")
    a = ap.parse_args()

    mark = ""
    if a.mark != "none":
        p = (BRAND / a.mark).resolve()
        if not p.exists():
            raise SystemExit(f"심볼 파일이 없습니다: {p}")
        mark = f'<div class="mark"><img src="file://{p}"></div>'

    sub = a.sub
    while "*" in sub:                      # *…* → <b>…</b>
        sub = sub.replace("*", "<b>", 1).replace("*", "</b>", 1)

    html = TPL.format(css=BRAND / "banner.css", palette=PALETTES[a.palette],
                      badge=a.badge, title=a.title.replace("|", "<br>"),
                      sub=sub, mark=mark)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html); tmp = f.name

    out = Path(a.out) if Path(a.out).is_absolute() else BRAND / a.out
    subprocess.run([str(WEBSHOT), "--url", f"file://{tmp}", "--output", str(out),
                    "--width", "1400", "--height", "400", "--dpr", "2", "--wait", "600"],
                   check=True)
    print(f"✓ {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
