/* RENEW 第5次の追加スクリプト。renew4.js の後に読み込む。動きは「動きを減らす」設定のときは付けない。 */
(function(){
  var d=document;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  /* 書籍・引用・重要な言葉：下からふわっと（一度だけ） */
  d.querySelectorAll('.book-card,.quote,.only-text,.cons-hero .free-note').forEach(function(el){
    if(el.hasAttribute('data-rv')||el.closest('.page-hero,.hero'))return;el.setAttribute('data-rv','');io.observe(el)});
  /* 3つの実績数値・3つのサービス：左から順に（時間差） */
  d.querySelectorAll('.nums3>div').forEach(function(el,i){el.style.setProperty('--d',i*120+'ms')});
  d.querySelectorAll('#services .svc-row').forEach(function(el,i){el.style.setProperty('--d',i*130+'ms')});
})();
