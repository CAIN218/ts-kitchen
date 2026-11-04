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
