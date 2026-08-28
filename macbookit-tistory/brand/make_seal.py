#!/usr/bin/env python3
"""맥부킷 도장(seal) 마크 생성 — 그래파이트 모노.

스퀘어클(연속 곡률 근사) 테두리 안에 「맥 부 / 킷 ⌘」 2×2.
디자인 정본: Blog-strategy/system/cupertino-design.md §9

사용:
  python3 make_seal.py                        # 도장 ink/light 2종을 1024px PNG 로
  python3 make_seal.py --size 512 --tone ink
  python3 make_seal.py --lockup               # 헤더 로고(도장+맥부킷 워드마크), 높이 128px=64@2x
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


def build_circle(size: int, tone: str, filled: bool = True) -> Image.Image:
    """원형 도장 — 프로필·대표 이미지용. 2×2 「맥 부 / 킷 ⌘」 를 원 안에 담는다.

    정본 §9 는 «정사각» 도장이지만, 프로필 자리는 플랫폼이 원형으로 깎는다.
    사각 도장을 그대로 넣으면 모서리 글자가 잘린다 → 원 전용 배치가 필요하다.
      filled=True   그래파이트 원 + 흰 글자   (배경이 뭐든 또렷하다 · 기본)
      filled=False  종이 원 + 그래파이트 테두리·글자 (잉크 도장에 가깝다)

    ⚠️ 16~32px(파비콘)에는 쓰지 않는다 — 2×2 가 뭉갠다. 그 자리는 --icon.
    """
    color = TONES[tone]
    paper = (255, 255, 255)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    box = (0, 0, size - 1, size - 1)
    if filled:
        d.ellipse(box, fill=color + (255,))
        ink = paper
        inner = size * 0.62          # 채운 원은 테두리가 없어 글자를 더 크게 쓴다
    else:
        stroke = max(2, round(size * 0.030))
        d.ellipse(box, fill=paper + (255,), outline=color + (255,), width=stroke)
        ink = color
        inner = size * 0.56

    cell = inner / 2
    ox = oy = (size - inner) / 2
    han = ImageFont.truetype(FONT, round(cell * 0.62), index=FONT_IDX)
    sym = ImageFont.truetype(FONT, round(cell * 0.70), index=FONT_IDX)

    for r, row in enumerate(GLYPHS):
        for c, ch in enumerate(row):
            font = han if "가" <= ch <= "힣" else sym
            cx = ox + cell * (c + 0.5)
            cy = oy + cell * (r + 0.5)
            bb = d.textbbox((0, 0), ch, font=font)
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1]), ch, font=font, fill=ink + (255,))
    return img


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


def build_icon(size: int, glyph: str = "맥") -> Image.Image:
    """파비콘·프로필용 «채운» 도장 — 그래파이트 바탕에 흰 글자 한 자.

    16~32px 에서는 2x2 네 글자가 뭉갠다. 아이콘은 한 글자만 남긴다.
    """
    ink = TONES["ink"]
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, size - 1, size - 1),
                        radius=round(size * 0.225), fill=ink + (255,))
    f = ImageFont.truetype(FONT, round(size * 0.60), index=6)  # Bold
    bb = d.textbbox((0, 0), glyph, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - w) / 2 - bb[0], (size - h) / 2 - bb[1]), glyph,
           font=f, fill=(255, 255, 255, 255))
    return img


def build_lockup(h: int, tone: str) -> Image.Image:
    """헤더 로고 — 도장 + 「맥부킷」 워드마크 가로 조합.

    티스토리 Book Club 스킨의 「로고(높이 64px)」에 넣는다.
    h=128 로 만들어 2x 로 쓴다(레티나).
    """
    color = TONES[tone]
    seal_side = round(h * 0.80)
    seal = build(seal_side, tone)

    gap = round(h * 0.17)
    word = "맥부킷"
    wf = ImageFont.truetype(FONT, round(h * 0.46), index=FONT_IDX)
    track = round(h * -0.012)  # 애플식 타이트 자간

    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    widths = [probe.textlength(c, font=wf) for c in word]
    word_w = round(sum(widths) + track * (len(word) - 1))

    img = Image.new("RGBA", (seal_side + gap + word_w, h), (0, 0, 0, 0))
    img.alpha_composite(seal, (0, (h - seal_side) // 2))

    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), word, font=wf)
    y = (h - (bb[3] - bb[1])) / 2 - bb[1]
    x = seal_side + gap
    for i, c in enumerate(word):
        d.text((x, y), c, font=wf, fill=color + (255,))
        x += widths[i] + track
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=1024)
    ap.add_argument("--tone", choices=list(TONES) + ["all"], default="all")
    ap.add_argument("--lockup", action="store_true",
                    help="헤더 로고(도장+워드마크). --size 는 «높이»로 해석(기본 128=64@2x)")
    ap.add_argument("--circle", action="store_true",
                    help="원형 도장(프로필·대표 이미지). 2×2 를 원 안에 담는다")
    ap.add_argument("--outline", action="store_true",
                    help="--circle 과 함께: 채우지 않고 종이 원 + 테두리로")
    ap.add_argument("--icon", action="store_true",
                    help="파비콘·프로필용 채운 아이콘(그래파이트 바탕 + 흰 「맥」)")
    ap.add_argument("--outdir", default=str(Path(__file__).parent))
    a = ap.parse_args()

    tones = list(TONES) if a.tone == "all" else [a.tone]
    if a.icon:
        n = a.size if a.size != 1024 else 512
        out = Path(a.outdir) / "icon-seal.png"
        build_icon(n).save(out)
        print(f"✓ {out}  ({n}x{n})")
        return
    if a.lockup:
        h = a.size if a.size != 1024 else 128
        for t in tones:
            out = Path(a.outdir) / f"logo-lockup-{t}.png"
            im = build_lockup(h, t)
            im.save(out)
            print(f"✓ {out}  ({im.width}x{im.height}, {t})")
        return
    for t in tones:
        out = Path(a.outdir) / f"seal-{t}.png"
        build(a.size, t).save(out)
        print(f"✓ {out}  ({a.size}px, {t})")


if __name__ == "__main__":
    main()
