/* RENEW 第8次：スマホの固定ボタン（renew7.js の置き換え）。renew6.js の後に読み込む。
   メニュー末尾の予約ボタン・フッター・フォームが画面に入る少し手前で固定ボタンを引っ込め、2つの予約ボタンが同時に見えないようにする。 */
(function(){
  var d=document,r=d.documentElement,page=d.body.getAttribute('data-page');
  /* コンサル：ページ内の「無料相談」ボタン（既存の文言そのまま）を、スマホでは画面下に固定表示 */
  if(page==='consulting'){var src=d.querySelector('.cons-cta .btn');if(src){var c=src.cloneNode(true);c.classList.add('cta-float');d.body.appendChild(c)}}
  /* ファーストビューを過ぎたら表示し、フッター・お問い合わせ・予約の案内が見えている間は隠す */
  var top=d.querySelector('.hero,.page-hero'),stops=d.querySelectorAll('footer,#contact,.menu-actions'),past=false,blocked=0;
  function upd(){r.classList.toggle('fab-on',past&&blocked===0)}
  if(!('IntersectionObserver' in window)){r.classList.add('fab-on');return}
  if(top)new IntersectionObserver(function(es){past=!es[0].isIntersecting;upd()},{threshold:0}).observe(top);
  var vis=new Set();var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)});blocked=vis.size;upd()},{threshold:0,rootMargin:'0px 0px 240px 0px'});
  stops.forEach(function(s){io.observe(s)});
})();

/* ───────── 沿革：HTMLの並び（2017→2026）どおりに、上から一度だけ表示する ───────── */
(function(){
  var d=document,tl=d.querySelector('.timeline');if(!tl)return;
  var lis=[].slice.call(tl.children),reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* 個別の表示（renew2.js）を外し、年表全体をひとつの流れとして扱う */
  lis.forEach(function(li,i){li.removeAttribute('data-rv');li.classList.remove('in');li.style.setProperty('--i',i)});
  /* 線の始点：各年のマーカーの中心（言語・画面幅で変わるので測る） */
  function mark(){lis.forEach(function(li){var t=li.querySelector('time');if(!t)return;
    var fs=parseFloat(getComputedStyle(t).fontSize),m=parseFloat(getComputedStyle(t,'::before').height)||11;
    li.style.setProperty('--mk',(t.getBoundingClientRect().top-li.getBoundingClientRect().top+fs*.62+m/2)+'px')})}
  mark();addEventListener('resize',mark);d.addEventListener('langchange',function(){setTimeout(mark,0)});if(d.fonts&&d.fonts.ready)d.fonts.ready.then(mark);
  tl.classList.add('tl-line');
  if(reduce||!('IntersectionObserver' in window)){tl.classList.add('tl-done');return}
  tl.classList.add('tl-wait');
  var io=new IntersectionObserver(function(es){var e=es[0];
    /* 画面に入った時、またはすでに通り過ぎていた時（高速スクロール・途中から再読込）に、まとめて開始 */
    if(e.isIntersecting||e.boundingClientRect.top<0){tl.classList.add('tl-go');io.disconnect();
      setTimeout(function(){tl.classList.add('tl-done')},lis.length*240+1200)}
  },{threshold:0,rootMargin:'0px 0px -12% 0px'});
  io.observe(tl);
})();

/* ───────── 日本語・英語の切り替えで、ボタン・ナビ・見出しの位置が動かないようにする ───────── */
(function(){
  var d=document,r=d.documentElement;
  /* 幅と高さを、両方の言語の大きいほうに揃える操作部品 */
  var CTRL=['.hd .nav a','.hd .lang','.hd-rsv','.drawer-foot .btn','.fab','.cta-float','.hero .row .btn','.cons-cta .btn',
    '.store-tabs button','.menu-stores button','.menu-actions .btn','.cater .row .btn','.cf7 button.btn'];
  /* 高さだけを揃える、ファーストビューの文章（左上の位置は変えない） */
  var TEXT=['.hero-in h1','.hero-in .hero-sub','.hero-in .sub','.page-hero h1','.page-hero .wrap > p'];
  function slots(sel){var els=[].slice.call(d.querySelectorAll(sel));
    if(els.length&&els.every(function(e){return e.hasAttribute('lang')}))return [els];/* 日英が別の要素のとき（トップの見出し）はひと組 */
    return els.map(function(e){return [e]})}
  function run(){
    var all=[],cur=r.getAttribute('data-lang')||'ja',oth=cur==='ja'?'en':'ja';
    CTRL.forEach(function(s){slots(s).forEach(function(g){all.push({g:g,w:1})})});
    TEXT.forEach(function(s){slots(s).forEach(function(g){all.push({g:g,w:0})})});
    all.forEach(function(o){o.g.forEach(function(e){e.style.minWidth='';e.style.minHeight=''})});
    function measure(){all.forEach(function(o){o.g.forEach(function(e){if(!e.getClientRects().length)return;var b=e.getBoundingClientRect();
      o.W=Math.max(o.W||0,b.width);o.H=Math.max(o.H||0,b.height)})})}
    measure();r.setAttribute('data-lang',oth);measure();r.setAttribute('data-lang',cur);
    all.forEach(function(o){o.g.forEach(function(e){
      /* 親の幅を超える場合は親の幅まで（スマホで画面からはみ出さない） */
      if(o.w&&o.W){var pa=e.parentElement,cs=getComputedStyle(pa),lim=pa.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);e.style.minWidth=Math.ceil(Math.min(o.W,lim>0?lim:o.W))+'px'}if(o.H)e.style.minHeight=Math.ceil(o.H)+'px'})});
    r.classList.add('lang-stable');
  }
  var t;function later(){clearTimeout(t);t=setTimeout(run,120)}
  run();addEventListener('resize',later);if(d.fonts&&d.fonts.ready)d.fonts.ready.then(run);
  d.addEventListener('langchange',later);
})();
