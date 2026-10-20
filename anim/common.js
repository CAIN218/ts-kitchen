/* デモ共通：切り替えバーと、スクロールで要素が見えたら .in を付ける仕組み */
(function(){
  window.TSK_REDUCED=matchMedia('(prefers-reduced-motion: reduce)').matches;
  try{history.scrollRestoration='manual'}catch(e){}
  var cur=document.documentElement.getAttribute('data-anim');
  var pg=document.documentElement.getAttribute('data-page')||'index';
  /* サブページ用：ブロック単位で表示するもの（入れ子で二重にならないよう葉の要素だけ） */
  window.TSK_SUB='.sec-in > h2, .sec-head, .body-lg, .quote, .ticks li, .svc-row, .dl-grid > div, .more, .book-card, .sub-h, .steps li, .only-text, .nums > div, .owner, .founder .muted, .contact .wrap > *, .blk .profile > *, .cv-box, .biz > div, .awards li, .menu-sec .wrap > *, .philosophy .wrap > *';
  window.TSK_HERO='.hero-in, .page-hero .wrap';
  var bar=document.createElement('nav');bar.className='demo-bar';bar.setAttribute('aria-label','アニメーション案の切り替え');
  [['a','案A ふわっと'],['a2','案A+ 追加版'],['b','案B 小麦をぬく'],['c','案C スクロール']].forEach(function(x){
    var a=document.createElement('a');a.href='anim-'+x[0]+(pg==='index'?'':'-'+pg)+'.html'+location.search;a.innerHTML=x[1].replace(/^(案[A-C]\+?) (.*)$/,'$1<span class="dn"> $2</span>');
    if(x[0]===cur)a.setAttribute('aria-current','page');bar.appendChild(a)});
  var r=document.createElement('button');r.type='button';r.textContent='↻ もう一度';
  r.addEventListener('click',function(){scrollTo(0,0);location.reload()});bar.appendChild(r);
  document.body.appendChild(bar);
  /* targets: セレクタ → 兄弟内の順番で少しずつ遅らせて表示 */
  window.tskReveal=function(sel,attr,step,viaParent){
    var els=document.querySelectorAll(sel);
    if(TSK_REDUCED||!('IntersectionObserver' in window))return;
    /* viaParent: clip-path で切り抜いた要素は自分では交差判定されないので、親が見えたら付ける */
    var kids=new Map();
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
      (kids.get(e.target)||[e.target]).forEach(function(k){k.classList.add('in')});io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(el){
      var n=0;
      for(var s=el.previousElementSibling;s;s=s.previousElementSibling)if(s.hasAttribute(attr))n++;
      el.setAttribute(attr,'');el.style.setProperty('--d',(n*(step||70))+'ms');
      var t=viaParent?el.parentNode:el;
      if(viaParent){if(!kids.has(t))kids.set(t,[]);kids.get(t).push(el)}
      io.observe(t)});
  };
})();
