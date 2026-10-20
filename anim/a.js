(function(){
  if(TSK_REDUCED)return;
  /* 見出しを1行ずつに分ける（言語ごとの span がある場合はその中身を分ける） */
  function lines(el){el.innerHTML=el.innerHTML.split(/<br\s*\/?>/i).map(function(t,i){return '<span class="ln"><span style="--i:'+i+'">'+t+'</span></span>'}).join('')}
  document.querySelectorAll('.hero h1, .page-hero h1').forEach(function(h){
    var ls=h.querySelectorAll(':scope > [lang]');ls.length?ls.forEach(lines):lines(h)});
  document.querySelectorAll('.page-hero .wrap > :not(h1)').forEach(function(e,i){e.style.setProperty('--k',i)});
  tskReveal('.about > img, .pt, section.blk h2, section.blk .lead, .policy, .card, .cater .tx > *, .flyer, .shopbox .tx > *, .shopbox .ph, .ig a, .badges li, '+TSK_SUB,'data-a',80);
})();
