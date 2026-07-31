# 실행 계획: GitHub (CDN) 기반 이미지 호스팅 및 SEO/접근성 정밀 최적화

## 1. 개요

이미 생성된 7개의 이미지를 `every-git/tistory-assets` 리포지토리에 업로드하고, **jsDelivr CDN**을 연동합니다. 또한 이미지의 파일명, `alt` 속성(대체 텍스트), 이미지 파손 시 대응 로직 등을 SEO와 웹 접근성 기준에 맞춰 최적화합니다.

## 2. 이미지 호스팅 및 CDN 전략

- **리포지토리**: `https://github.com/every-git/tistory-assets.git` (Public)
- **CDN**: `https://cdn.jsdelivr.net/gh/every-git/tistory-assets@main/images/[파일명]`
- **상태**: 공개형 리포지토리를 통한 외부 로딩 보장.

## 3. 이미지별 SEO 및 접근성 상세 매핑

| 원본 파일명 | 변경된 SEO 파일명 | `alt` 속성 (이미지 설명/깨짐 시 노출) | 이미지 캡션 (`figcaption`) |
| :--- | :--- | :--- | :--- |
| `hero_macbook_battery.png` | `macbook-battery-life-extension-settings-hero.png` | 맥북 배터리 수명 연장 설정 5가지 가이드 대표 이미지 | 맥북 배터리 수명을 극대화하는 5가지 핵심 설정 가이드 |
| `setting_optimized_charging.png` | `macos-optimized-battery-charging-ui-setting.png` | macOS 시스템 설정 내 최적화된 배터리 충전 기능 활성화 화면 | ① 최적화된 배터리 충전 기능을 켜서 과충전을 방지하세요 |
| `setting_low_power_mode.png` | `macbook-low-power-mode-절전-icon.png` | 맥북 저전력 모드 활성화로 에너지 효율을 높이는 아이콘 | ② 배터리 사용 시 저전력 모드가 자동으로 켜지도록 설정합니다 |
| `setting_display_background.png` | `macbook-display-brightness-background-apps-monitoring.png` | 디스플레이 밝기 조절 및 백그라운드 배터리 소모 앱 감시 도구 | ③ 화면 밝기를 최적화하고 에너지를 많이 쓰는 앱을 종료하세요 |
| `setting_battery_cycle.png` | `macbook-battery-cycle-count-check-guide.png` | 맥북 시스템 정보에서 배터리 사이클 수를 확인하는 방법 아이콘 | ④ 내 맥북의 현재 배터리 건강 상태(사이클 수)를 확인하세요 |
| `setting_adapter_tip.png` | `macbook-m1-m2-m3-power-adapter-charging-tips.png` | 맥북 전원 어댑터 연결 상태에서의 배터리 관리 시스템(BMS) 원리 | ⑤ 전원 어댑터 상시 연결 시에도 배터리는 안전하게 보호됩니다 |
| `faq_icon.png` | `macbook-battery-frequently-asked-questions-faq-3d.png` | 맥북 배터리에 대해 가장 자주 묻는 질문과 답변(FAQ) 아이콘 | ❓ 맥북 배터리 관리에 대해 궁금한 점을 해결해 드립니다 |

## 4. 기술적 구현 및 예외 처리

### 4.1. 이미지 태그 구조 (SEO & Fallback)
이미지가 깨졌을 경우를 대비하여 다음 구조를 적용합니다:
```html
<figure style="text-align: center; margin: 2rem 0;">
  <img src="[CDN 주소]" 
       alt="[이미지 설명]" 
       title="[이미지 제목]" 
       onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" 
       style="max-width: 80%; height: auto; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
  <div style="display:none; padding: 20px; background: #f9f9f9; border-radius: 12px;">🖼️ 이미지를 불러올 수 없습니다: [이미지 설명]</div>
  <figcaption style="font-size: 0.9rem; color: #666; margin-top: 10px;">[이미지 캡션]</figcaption>
</figure>
```

### 4.2. Todo List
- [ ] 이미지 파일명 SEO 기준 일괄 변경 (파일 리네임)
- [ ] 로컬 Git 저장소 초기화 및 `every-git/tistory-assets` 원격 연결
- [ ] GitHub 푸시 (CLI 명령)
- [ ] HTML 파일 내 모든 이미지 태그를 SEO/CDN 구조로 대규모 업데이트 (복합 치환)
- [ ] 최종 결과물 티스토리 삽입 테스트 가이드

---
**의견**: 이미지 설명뿐만 아니라 깨졌을 때의 대체 텍스트와 레이아웃 유지 전략까지 포함했습니다. 승인해 주시면 진행하겠습니다.
