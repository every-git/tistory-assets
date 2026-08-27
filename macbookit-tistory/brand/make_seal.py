#!/usr/bin/env python3
"""맥부킷 도장(seal) 마크 생성 — 그래파이트 모노.

스퀘어클(연속 곡률 근사) 테두리 안에 「맥 부 / 킷 ⌘」 2×2.
디자인 정본: Blog-strategy/system/cupertino-design.md §9

사용:
  python3 make_seal.py                       # ink/light 2종을 1024px PNG 로
  python3 make_seal.py --size 512 --tone ink
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_IDX = 4  # SemiBold
TONES = {
    "ink":   (29, 29, 31),      # #1D1D1F — 밝은 이미지·본문용
    "light": (245, 245, 247),   # #F5F5F7 — 어두운 스크린샷용
}
GLYPHS = (("맥", "부"), ("킷", "⌘"))


def squircle(draw, box, radius, color, width):
    """Pillow 의 rounded_rectangle 로 애플식 큰 라운드 사각을 그린다."""
    draw.rounded_rectangle(box, radius=radius, outline=color, width=width)


def build(size: int, tone: str) -> Image.Image:
    color = TONES[tone]
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    stroke = max(2, round(size * 0.032))
    pad = round(size * 0.045)
    box = (pad, pad, size - pad - 1, size - pad - 1)
    radius = round(size * 0.225)
    squircle(d, box, radius, color + (255,), stroke)

    inner = size - 2 * pad - 2 * stroke
    cell = inner / 2
    # 글자는 칸 높이의 58% — 도장은 글자가 꽉 차야 도장으로 보인다
    han = ImageFont.truetype(FONT, round(cell * 0.58), index=FONT_IDX)
    # ⌘ 같은 기호는 같은 사이즈에서 옵티컬하게 작게 보인다 → 한 단계 키운다
    sym = ImageFont.truetype(FONT, round(cell * 0.66), index=FONT_IDX)

    for r, row in enumerate(GLYPHS):
        for c, ch in enumerate(row):
            font = han if "가" <= ch <= "힣" else sym
            cx = pad + stroke + cell * (c + 0.5)
            cy = pad + stroke + cell * (r + 0.5)
            bb = d.textbbox((0, 0), ch, font=font)
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1]), ch,
                   font=font, fill=color + (255,))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=1024)
    ap.add_argument("--tone", choices=list(TONES) + ["all"], default="all")
    ap.add_argument("--outdir", default=str(Path(__file__).parent))
    a = ap.parse_args()

    tones = list(TONES) if a.tone == "all" else [a.tone]
    for t in tones:
        out = Path(a.outdir) / f"seal-{t}.png"
        build(a.size, t).save(out)
        print(f"✓ {out}  ({a.size}px, {t})")


if __name__ == "__main__":
    main()
