/* デモ共通：切り替えバーと、スクロールで要素が見えたら .in を付ける仕組み */
(function(){
  window.TSK_REDUCED=matchMedia('(prefers-reduced-motion: reduce)').matches;
  try{history.scrollRestoration='manual'}catch(e){}
  var cur=document.documentElement.getAttribute('data-anim');
  var bar=document.createElement('nav');bar.className='demo-bar';bar.setAttribute('aria-label','アニメーション案の切り替え');
  [['a','案A ふわっと'],['b','案B 小麦をぬく'],['c','案C スクロール']].forEach(function(x){
    var a=document.createElement('a');a.href='anim-'+x[0]+'.html'+location.search;a.innerHTML=x[1].replace(/^(案.) (.*)$/,'$1<span class="dn"> $2</span>');
    if(x[0]===cur)a.setAttribute('aria-current','page');bar.appendChild(a)});
  var r=document.createElement('button');r.type='button';r.textContent='↻ もう一度';
  r.addEventListener('click',function(){scrollTo(0,0);location.reload()});bar.appendChild(r);
  document.body.appendChild(bar);
  /* targets: セレクタ → 兄弟内の順番で少しずつ遅らせて表示 */
  window.tskReveal=function(sel,attr,step){
    var els=document.querySelectorAll(sel);
    if(TSK_REDUCED||!('IntersectionObserver' in window))return;
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(el){
      var n=0,p=el.parentNode;
      for(var s=el.previousElementSibling;s;s=s.previousElementSibling)if(s.hasAttribute(attr))n++;
      el.setAttribute(attr,'');el.style.setProperty('--d',(n*(step||70))+'ms');io.observe(el)});
  };
})();
