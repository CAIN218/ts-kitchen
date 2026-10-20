(function(){
  if(TSK_REDUCED)return;
  var hd=document.querySelector('.hd'),root=document.documentElement,tk=false;
  function upd(){tk=false;var y=scrollY;if(y<900)root.style.setProperty('--sy',y);hd.classList.toggle('scrolled',y>40)}
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd();
  tskReveal('.about img, .flyer, .shopbox .ph, .card .ph, .ig a','data-c',90);
  tskReveal('section.blk h2','data-t',0);
  tskReveal('section.blk .lead, .pt, .policy, .cater .tx > *:not(h2), .shopbox .tx > *:not(h2), .badges li','data-s',90);
  /* 店舗タブのスライドする丸 */
  var tabs=document.querySelector('.store-tabs');
  if(tabs){
    var ind=document.createElement('span');ind.className='ind';tabs.insertBefore(ind,tabs.firstChild);
    var place=function(){var b=tabs.querySelector('[aria-selected=true]');if(!b||!b.offsetWidth)return;ind.style.width=b.offsetWidth+'px';ind.style.transform='translateX('+b.offsetLeft+'px)'};
    tabs.addEventListener('click',function(){requestAnimationFrame(place)});
    addEventListener('resize',place);document.fonts&&document.fonts.ready.then(place);place();
  }
})();
