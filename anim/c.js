(function(){
  if(TSK_REDUCED)return;
  var hd=document.querySelector('.hd'),root=document.documentElement,tk=false;
  function upd(){tk=false;var y=scrollY;if(y<900)root.style.setProperty('--sy',y);hd.classList.toggle('scrolled',y>40)}
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd();
  document.querySelectorAll('.page-hero .wrap > *').forEach(function(e,i){e.style.setProperty('--k',i)});
  tskReveal('.about img, .flyer, .shopbox .ph, .card .ph, .ig a, .owner img, .biz .ph','data-c',90,true);
  tskReveal('main h2','data-t',0);
  tskReveal('section.blk .lead, .pt, .policy, .cater .tx > *:not(h2), .shopbox .tx > *:not(h2), .badges li, '+TSK_SUB.replace('.sec-in > h2, ','').replace('.owner, ','').replace('.contact .wrap > *','.contact .wrap > *:not(h2)'),'data-s',90);
  /* 数字は0からカウントアップ（実績の数字そのものは変えない） */
  document.querySelectorAll('.nums b').forEach(function(b){
    var t=b.firstChild;if(!t||t.nodeType!==3)return;var to=parseInt(t.nodeValue,10);if(!to)return;t.nodeValue='0';
    var io=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;io.disconnect();var s=performance.now();
      (function f(n){var p=Math.min((n-s)/1400,1);t.nodeValue=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)})(s)},{threshold:.6});io.observe(b)});
  /* 店舗タブのスライドする丸 */
  var tabs=document.querySelector('.store-tabs');
  if(tabs){
    var ind=document.createElement('span');ind.className='ind';tabs.insertBefore(ind,tabs.firstChild);
    var place=function(){var b=tabs.querySelector('[aria-selected=true]');if(!b||!b.offsetWidth)return;ind.style.width=b.offsetWidth+'px';ind.style.transform='translateX('+b.offsetLeft+'px)'};
    tabs.addEventListener('click',function(){requestAnimationFrame(place)});
    addEventListener('resize',place);document.fonts&&document.fonts.ready.then(place);place();
  }
})();
