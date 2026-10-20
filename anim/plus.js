(function(){
  if(TSK_REDUCED)return;
  /* ヘッダー */
  var hd=document.querySelector('.hd'),tk=false;
  function upd(){tk=false;hd.classList.toggle('scrolled',scrollY>40)}
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd();
  /* 小麦（茎と粒）に斜線を重ねる */
  var g='';for(var i=0;i<6;i++){var y=18+i*13;g+='<ellipse class="gr" cx="12" cy="'+y+'" rx="5" ry="9" transform="rotate(-28 12 '+y+')"/><ellipse class="gr" cx="28" cy="'+y+'" rx="5" ry="9" transform="rotate(28 28 '+y+')"/>'}
  g+='<ellipse class="gr" cx="20" cy="6" rx="4.5" ry="9"/><rect class="gr" x="19" y="20" width="2.4" height="100"/>';
  var hero=document.querySelector('.hero,.page-hero');
  if(hero){
    var f=document.createElement('div');f.className='p-field';f.setAttribute('aria-hidden','true');
    var rot=[-6,4,-3];
    for(var k=0;k<3;k++){var d=document.createElement('div');d.className='p-w s'+k;
      d.style.cssText='--r:'+rot[k]+'deg;--t:'+(.9+k*.15)+'s;--s:'+(2.2+k*.3)+'s;--o:'+(4.1+k*.3)+'s';
      d.innerHTML='<svg class="tsk-wheat" viewBox="0 0 40 120" style="width:100%;height:100%">'+g+'<path class="sl" d="M2 108 L38 12"/></svg>';f.appendChild(d)}
    hero.insertBefore(f,hero.firstChild)}
  /* 店舗タブのスライドする丸 */
  var tabs=document.querySelector('.store-tabs');
  if(tabs){
    var ind=document.createElement('span');ind.className='ind';tabs.insertBefore(ind,tabs.firstChild);
    var place=function(){var b=tabs.querySelector('[aria-selected=true]');if(!b||!b.offsetWidth)return;ind.style.width=b.offsetWidth+'px';ind.style.transform='translateX('+b.offsetLeft+'px)'};
    tabs.addEventListener('click',function(){requestAnimationFrame(place)});
    addEventListener('resize',place);document.fonts&&document.fonts.ready.then(place);place();
  }
  /* 実績の数字は0から数え上がる（数字そのものは変えない） */
  document.querySelectorAll('.nums b').forEach(function(b){
    var t=b.firstChild;if(!t||t.nodeType!==3)return;var to=parseInt(t.nodeValue,10);if(!to)return;t.nodeValue='0';
    var io=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;io.disconnect();var s=performance.now();
      (function f(n){var p=Math.min((n-s)/1400,1);t.nodeValue=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)})(s)},{threshold:.6});io.observe(b)});
})();
