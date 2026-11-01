/* 改修デモ v2 の追加スクリプト。script.js と anim/site.js の後に読み込む。 */
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* 全要素を動かさず、重要な部分だけにする：小さな要素は動かさず、親の節ごとに現れる */
  if(!reduce){
    document.querySelectorAll('.ig a, .badges li, .awards li, .ticks li, .steps li, .biz > div, .nums > div, .dl-grid > div, .svc-row, .pt, .policy').forEach(function(e){
      e.removeAttribute('data-a');e.style.removeProperty('--d');
    });
  }
  /* 店舗タブ：キーボードの左右キーでも切り替えられる */
  var tabs=document.querySelector('.store-tabs');
  if(tabs){
    tabs.setAttribute('role','tablist');
    tabs.addEventListener('keydown',function(e){
      if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
      var bs=[].slice.call(tabs.querySelectorAll('button')),i=bs.indexOf(document.activeElement);
      if(i<0)return;var n=bs[(i+(e.key==='ArrowRight'?1:bs.length-1))%bs.length];n.focus();n.click();e.preventDefault();
    });
  }

  /* サブページ：重要なブロックだけ、下からそっと現れる（スクロールで1回） */
  if(!reduce&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1,rootMargin:'0px 0px -6% 0px'});
    var n=0;document.querySelectorAll('.notice,.menu-stores,.menu-cats,.menu-view,.menu-actions,.cf7,.sec-head,.philosophy h2,.profile,.timeline,.biz,.nums,.cv-box,.owner,.quote').forEach(function(el){
      if(el.hasAttribute('data-a'))return;el.setAttribute('data-a','');el.style.setProperty('--d',((n++%3)*80)+'ms');io.observe(el)});
  }
  /* メニュー画像の切り替え：やわらかく差し替わる */
  var mv=document.querySelector('.menu-view');
  if(mv)document.querySelectorAll('.menu-stores button,.menu-cats').forEach(function(b){b.addEventListener('click',function(){setTimeout(function(){mv.classList.remove('sw');void mv.offsetWidth;mv.classList.add('sw')},0)})});
})();
