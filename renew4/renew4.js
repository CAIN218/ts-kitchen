/* RENEW 第4次の追加スクリプト。renew/renew.js → renew2/renew2.js の後に読み込む。 */
(function(){
  var d=document,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* 画像の拡大（メニューのライトボックス）：もう一度タップで等倍／拡大を切り替え */
  var lb=d.getElementById('lightbox'),img=d.getElementById('lbImg');
  if(lb&&img){
    img.addEventListener('click',function(e){e.stopPropagation();lb.classList.toggle('zoom')});
    new MutationObserver(function(){if(lb.hidden)lb.classList.remove('zoom')}).observe(lb,{attributes:true,attributeFilter:['hidden']});
  }
  /* 追加したまとまりの、スクロール表示（一度だけ） */
  if(reduce||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1,rootMargin:'0px 0px -6% 0px'});
  d.querySelectorAll('.about-ph,.cater-vis').forEach(function(el){
    if(el.hasAttribute('data-rv'))return;el.setAttribute('data-rv','');io.observe(el)});
  /* 会社の沿革：上から順に点がともる */
  d.querySelectorAll('.timeline li').forEach(function(li,i){li.style.setProperty('--d',Math.min(i%4,3)*90+'ms')});
})();
