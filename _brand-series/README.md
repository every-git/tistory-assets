# 계열 프로필 로고 시리즈 (2026-08-28)

네 블로그가 **하나의 조형 언어**를 공유한다. 프로필·대표 이미지 전용.

| 블로그 | 파일 | 색 | 심볼 |
|---|---|---|---|
| 맥부킷 | `macbookit-tistory/brand/profile-circle.png` | 그래파이트 `#1D1D1F` | ⌘ 커맨드 |
| 도와줘요 경자씨 | `kyungja-tistory/brand/profile-circle.png` | 경자그린 `#1E6E46` | 상승 막대 |
| apply (예정) | `_brand-series/logo-apply.png` | 슬레이트 `#2F4F6F` | 서류+체크 |
| car (예정) | `_brand-series/logo-car.png` | 번트클레이 `#A8452A` | 차 실루엣 |

**공통 규칙** — 원형 배지 · 단색 채움 · 흰 심볼 하나 · **그림자 0 · 그라디언트 0 · 글자 0**
· 512×512 RGBA(원 밖 투명) · 심볼은 원 가장자리에 닿지 않는다.

생성: `/image-gen` (gpt-image-2) → 흰 배경 생성 후 원형 알파 마스킹.
색은 각 브랜드 정본 값을 그대로 쓴다(`cupertino-design.md` §2 ink · `paper-ink` 경자그린).

⚠️ **파비콘(16~32px)에는 쓰지 않는다.** 심볼이 뭉갠다 —
맥부킷 파비콘은 `make_seal.py --icon`(「맥」 한 글자)을 유지한다.
