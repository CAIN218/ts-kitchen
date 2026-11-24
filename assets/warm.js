/* Warm Editorial デモ共通：スマホの固定予約ボタンを、ヒーローの予約ボタンや店舗一覧が見えている間は引っ込める
   （renew14.js の判定に重ねて、html に warm-stop を付け外しする。CSS 側で .warm-stop のとき .fab を隠す） */
(function(){
  var d=document,r=d.documentElement;if(!('IntersectionObserver' in window))return;
  var t=d.querySelectorAll('.hero .row,#stores .cards,#contact');if(!t.length)return;
  var vis=new Set();
  var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)});r.classList.toggle('warm-stop',vis.size>0)},{threshold:0});
  t.forEach(function(el){io.observe(el)});
})();
