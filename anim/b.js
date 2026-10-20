(function(){
  if(TSK_REDUCED)return;
  /* 小麦：茎と粒を重ねた線画。上に斜線(.sl)を重ねる */
  var g='';for(var i=0;i<6;i++){var y=18+i*13;g+='<ellipse class="gr" cx="12" cy="'+y+'" rx="5" ry="9" transform="rotate(-28 12 '+y+')"/><ellipse class="gr" cx="28" cy="'+y+'" rx="5" ry="9" transform="rotate(28 28 '+y+')"/>'}
  g+='<ellipse class="gr" cx="20" cy="6" rx="4.5" ry="9"/><rect class="gr" x="19" y="20" width="2.4" height="100"/>';
  function svg(cls,extra){return '<svg class="'+cls+'" viewBox="0 0 40 120" aria-hidden="true" '+(extra||'')+'>'+g+'<path class="sl" d="M2 108 L38 12"/></svg>'}
  var hero=document.querySelector('.hero,.page-hero');
  var f=document.createElement('div');f.className='b-field';f.setAttribute('aria-hidden','true');
  var rot=[-6,4,-3,7,-8];
  for(var k=0;k<5;k++){
    var d=document.createElement('div');d.className='b-w s'+k;
    d.style.cssText='--r:'+rot[k]+'deg;--t:'+(.2+k*.15)+'s;--s:'+(1.7+k*.28)+'s;--o:'+(3.6+k*.28)+'s';
    d.innerHTML=svg('tsk-wheat','style="width:100%;height:100%"');f.appendChild(d)}
  hero.insertBefore(f,hero.firstChild);
  /* ポイントのアイコン（1つ目：小麦などを使わない） */
  var pt=document.querySelector('.pt b');
  if(pt)pt.insertAdjacentHTML('beforebegin',svg('ico tsk-wheat'));
  /* 進み具合のバー */
  var bar=document.createElement('div');bar.className='b-prog';document.body.appendChild(bar);
  var tk=false;function upd(){tk=false;var h=document.documentElement.scrollHeight-innerHeight;bar.style.transform='scaleX('+(h>0?scrollY/h:0)+')'}
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd();
  document.querySelectorAll('.page-hero .wrap > *').forEach(function(e,i){e.style.setProperty('--k',i)});
  tskReveal('main h2','data-b',0);
  tskReveal('.about > img, .pt, section.blk .lead, .policy, .card, .cater .tx > *:not(h2), .flyer, .shopbox .tx > *:not(h2), .shopbox .ph, .ig a, .badges li, '+TSK_SUB.replace('.sec-in > h2, ','').replace('.contact .wrap > *','.contact .wrap > *:not(h2)'),'data-b',90);
  document.querySelectorAll('main h2').forEach(function(h){h.removeAttribute('data-b')});
})();
