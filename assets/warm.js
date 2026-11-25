/* Warm Editorial デモ共通：スマホの固定予約ボタンを、ヒーローの予約ボタンや店舗一覧が見えている間は引っ込める
   （renew14.js の判定に重ねて、html に warm-stop を付け外しする。CSS 側で .warm-stop のとき .fab を隠す） */
(function(){
  var d=document,r=d.documentElement;if(!('IntersectionObserver' in window))return;
  /* 案C（4回目）：固定ボタンの出し入れは warm-c.js の1つの仕組みにまとめたので、ここでは何もしない */
  if(r.getAttribute('data-warm')==='c')return;
  /* 案C：店舗ごとの予約ボタンをやめ、店舗欄の最後に共通の予約ボタン（.stores-rsv）を置いた。店舗欄を読んでいる間は固定ボタンを出し、共通ボタンが見えたら引っ込める。ケータリングの「メールで相談する」と同時に見えないよう、#catering の間も引っ込める。公式SNS（.sns-sec）の右下の YouTube に重なるので、そこでも引っ込める */
  var c=d.querySelector('.stores-rsv');
  var t=d.querySelectorAll(c?'.hero .row,.stores-rsv,#catering,#contact,.sns-sec':'.hero .row,#stores .cards,#contact');if(!t.length)return;
  var vis=new Set();
  var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)});r.classList.toggle('warm-stop',vis.size>0)},{threshold:0});
  t.forEach(function(el){io.observe(el)});
})();
