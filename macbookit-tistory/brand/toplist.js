/* 맥부킷 — 글 화면 상단 「전체보기」 목록
   2026-08-28. 네이버 블로그는 글 화면에서도 위에 목록을 보여준다. 그 문법을 옮겼다.

   ⚠️ 티스토리 치환자 <s_rctps_rep> 는 «사이드바 모듈 안에서만» 최근글로 채워진다.
      <s_permalink_article_rep> 안에 쓰면 현재 글이 5번 반복된다(2026-08-28 실측).
      그래서 같은 도메인의 /rss 를 읽어 채운다 — CORS 없고 파싱이 안정적이다. */

(function () {
  var box = document.querySelector('.post-toplist');
  if (!box) return;
  var ul = box.querySelector('ul');
  if (!ul) return;

  var here = location.pathname.replace(/\/$/, '');

  fetch('/rss', { credentials: 'same-origin' })
    .then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); })
    .then(function (xml) {
      var doc = new DOMParser().parseFromString(xml, 'application/xml');
      var items = [].slice.call(doc.querySelectorAll('item'));
      // ⚠️ 티스토리 RSS 는 제목을 «이중 인코딩»한다 — XML 을 풀어도 &mdash; 가 남는다.
      //    한 번 더 디코드하지 않으면 목록에 &mdash;·&middot; 가 그대로 보인다(2026-08-28 실측).
      var dec = function (x) { var t = document.createElement('textarea'); t.innerHTML = x; return t.value; };
      var rows = [];
      for (var i = 0; i < items.length && rows.length < 5; i++) {
        var link = (items[i].querySelector('link') || {}).textContent || '';
        var path = link.replace(/^https?:\/\/[^/]+/, '').replace(/\/$/, '');
        if (path === here) continue;                 // 지금 보고 있는 글은 뺀다
        var title = dec((items[i].querySelector('title') || {}).textContent || '');
        var d = new Date((items[i].querySelector('pubDate') || {}).textContent || '');
        var date = isNaN(d) ? '' :
          d.getFullYear() + '. ' + (d.getMonth() + 1) + '. ' + d.getDate() + '.';
        rows.push({ link: link, title: title, date: date });
      }
      if (!rows.length) { box.style.display = 'none'; return; }

      var frag = document.createDocumentFragment();
      rows.forEach(function (r) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = r.link;
        var t = document.createElement('span'); t.className = 't'; t.textContent = r.title;
        var s = document.createElement('span'); s.className = 'd'; s.textContent = r.date;
        a.appendChild(t); a.appendChild(s); li.appendChild(a); frag.appendChild(li);
      });
      ul.innerHTML = '';
      ul.appendChild(frag);
      box.classList.add('is-ready');
    })
    .catch(function () { box.style.display = 'none'; });  // 실패하면 조용히 감춘다
})();

/* 카테고리를 body 클래스로 옮긴다 — 스킨 CSS 는 카테고리를 모른다.
   맥부킷은 «색이 카테고리를 가르므로»(Claude code=크림·클레이 / Apple & Mac=흰·블루)
   본문 바탕색을 이 클래스로 고른다. */
(function () {
  var el = document.querySelector('.post-byline .category, .post-cover .category');
  if (!el) return;
  var key = el.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  if (key) document.body.classList.add('cat-' + key);
})();
