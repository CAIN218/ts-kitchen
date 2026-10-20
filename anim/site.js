(function(){
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  /* 見出しを1行ずつに分ける（言語ごとの span がある場合は、その中身を分ける） */
  function lines(el){el.innerHTML=el.innerHTML.split(/<br\s*\/?>/i).map(function(t,i){return '<span class="ln"><span style="--i:'+i+'">'+t+'</span></span>'}).join('')}
  document.querySelectorAll('.hero h1, .page-hero h1').forEach(function(h){var ls=h.querySelectorAll(':scope > [lang]');ls.length?ls.forEach(lines):lines(h)});
  document.querySelectorAll('.page-hero .wrap > :not(h1)').forEach(function(e,i){e.style.setProperty('--k',i)});
  /* スクロールで見えたブロックに .in を付ける */
  var SEL='.about > img, .pt, section.blk h2, section.blk .lead, .policy, .card, .cater .tx > *, .flyer, .shopbox .tx > *, .shopbox .ph, .ig a, .badges li, .sec-in > h2, .sec-head, .body-lg, .quote, .ticks li, .svc-row, .dl-grid > div, .more, .book-card, .sub-h, .steps li, .only-text, .nums > div, .owner, .founder .muted, .contact .wrap > *, .blk .profile > *, .cv-box, .biz > div, .awards li, .menu-sec .wrap > *, .philosophy .wrap > *';
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    document.querySelectorAll(SEL).forEach(function(el){var n=0;for(var s=el.previousElementSibling;s;s=s.previousElementSibling)if(s.hasAttribute('data-a'))n++;el.setAttribute('data-a','');el.style.setProperty('--d',(n*80)+'ms');io.observe(el)});
  }
  /* ヘッダーがスクロールで少し細くなる */
  var hd=document.querySelector('.hd'),tk=false;
  function upd(){tk=false;if(hd)hd.classList.toggle('scrolled',scrollY>40)}
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd();
  /* 店舗タブのスライドする丸 */
  var tabs=document.querySelector('.store-tabs');
  if(tabs){
    var ind=document.createElement('span');ind.className='ind';tabs.insertBefore(ind,tabs.firstChild);
    var place=function(){var b=tabs.querySelector('[aria-selected=true]');if(!b||!b.offsetWidth)return;ind.style.width=b.offsetWidth+'px';ind.style.transform='translateX('+b.offsetLeft+'px)'};
    tabs.addEventListener('click',function(){requestAnimationFrame(place)});
    addEventListener('resize',place);document.fonts&&document.fonts.ready.then(place);place();
  }
  /* 実績の数字は0から数え上がる（数字そのものは変えない） */
  document.querySelectorAll('.nums b').forEach(function(b){
    var t=b.firstChild;if(!t||t.nodeType!==3)return;var to=parseInt(t.nodeValue,10);if(!to)return;t.nodeValue='0';
    var o=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;o.disconnect();var s=performance.now();(function f(n){var p=Math.min((n-s)/1400,1);t.nodeValue=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)})(s)},{threshold:.6});o.observe(b)});
})();
