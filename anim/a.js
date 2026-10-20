(function(){
  if(TSK_REDUCED)return;
  document.querySelectorAll('.hero h1').forEach(function(h){
    h.innerHTML=h.innerHTML.split(/<br\s*\/?>/i).map(function(t,i){return '<span class="ln"><span style="--i:'+i+'">'+t+'</span></span>'}).join('');
  });
  tskReveal('.about > img, .pt, section.blk h2, section.blk .lead, .policy, .card, .cater .tx > *, .flyer, .shopbox .tx > *, .shopbox .ph, .ig a, .badges li','data-a',80);
})();
