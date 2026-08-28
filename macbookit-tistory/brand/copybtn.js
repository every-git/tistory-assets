/* 맥부킷 스킨 — 코드블록 복사 버튼 + 선택 해제
   2026-08-28. tistory-style.md §4-b: 「복사 버튼은 스킨 JS 가 자동으로 붙인다」
   ⚠️ 우클릭 금지 스크립트(스킨 HTML 16~34행)는 type="text/plain" 으로 무력화했다.
      되돌리려면 그 한 단어를 javascript 로 되돌린다. */

/* 버튼 색은 «카테고리»를 따라간다(2026-08-28 사용자 지시: 색상은 분리한다).
   스킨 JS 는 카테고리를 모르므로 조판이 이미 칠해 둔 «코드블록 바탕색»으로 판별한다.
   #F0EEE6(클로드 크림) → 클레이 · 그 밖(#F5F5F7 등) → 애플 블루. */
document.addEventListener('DOMContentLoaded', function () {
  var CLAY = '#A8452A', BLUE = '#0066CC';
  document.querySelectorAll('pre').forEach(function (pre) {
    if (pre.dataset.copyReady) return;
    pre.dataset.copyReady = '1';
    var code = pre.querySelector('code');
    var bg = code ? getComputedStyle(code).backgroundColor.replace(/\s/g, '') : '';
    var accent = (bg === 'rgb(240,238,230)') ? CLAY : BLUE;
    var text = (code || pre).innerText;
    pre.style.position = 'relative';
    var b = document.createElement('button');
    b.type = 'button';
    b.textContent = '복사';
    b.setAttribute('aria-label', '코드 복사');
    b.style.cssText = 'position:absolute;top:12px;right:12px;padding:6px 12px;font-size:12px;'
      + 'font-weight:700;color:' + accent + ';background:#fff;border:1px solid #cfcdc6;'
      + 'border-radius:6px;cursor:pointer;line-height:1;z-index:2;box-shadow:0 1px 3px rgba(0,0,0,.08)';
    b.addEventListener('click', function () {
      var done = function () {
        b.textContent = '복사됨'; b.style.color = '#fff'; b.style.background = accent;
        setTimeout(function () {
          b.textContent = '복사'; b.style.color = accent; b.style.background = '#fff';
        }, 1500);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select();
        document.execCommand('copy'); document.body.removeChild(ta); done();
      }
    });
    pre.appendChild(b);
  });
});

/* 맥부킷 — 코드블록에서만 선택·복사를 되살린다.
   우클릭 금지 스크립트가 document 에 selectstart·contextmenu 를 걸어 두는데,
   명령어 글에서 «복사»가 막히면 글의 쓸모가 사라진다.
   본문 전체를 푸는 대신 pre/code 안에서만 이벤트 전파를 끊는다. */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('pre, pre code').forEach(function (el) {
    el.style.userSelect = 'text';
    el.style.webkitUserSelect = 'text';
    ['selectstart', 'contextmenu', 'dragstart', 'copy'].forEach(function (ev) {
      el.addEventListener(ev, function (e) { e.stopPropagation(); }, true);
    });
  });
});
