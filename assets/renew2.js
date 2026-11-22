/* RENEW 第2次の追加スクリプト。renew/renew.js の後に読み込む。動きは「動きを減らす」設定のときは付けない。 */
(function(){
  var d=document,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* 店舗・メニューのタブ：オレンジの線が選択位置へ滑らかに動く */
  function tabInd(el){
    if(!el)return;var ind=d.createElement('span');ind.className='tab-ind';el.appendChild(ind);
    function place(anim){var b=el.querySelector('[aria-selected=true]');if(!b||!b.offsetWidth)return;
      ind.classList.toggle('on',!!anim);ind.style.width=b.offsetWidth+'px';ind.style.transform='translateX('+b.offsetLeft+'px)'}
    el.addEventListener('click',function(){requestAnimationFrame(function(){place(true)})});
    addEventListener('resize',function(){place(false)});
    d.addEventListener('langchange',function(){setTimeout(function(){place(false)},0)});
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(function(){place(false)});
    place(false);
  }
  tabInd(d.querySelector('.store-tabs'));tabInd(d.querySelector('.menu-stores'));
  /* スクロール表示：まとまり（セクション・写真・一覧）ごとに、一度だけ */
  if(reduce||!('IntersectionObserver' in window))return;
  var SEL=['main section .wrap > h2','main section .wrap > .lead','.about > img','.about .lead','.points','.store-tabs','.cards','.policy',
    '.cater .tx','.flyer','.shopbox .ph','.shopbox .tx','.ig','.badges','.profile > *','.philosophy .wrap > *','.nums > div','.cv-box',
    '.biz > div','.timeline li','.media > *','.sec-in > *','.svc-row','.dl-grid > div','.steps li','.only-text','.quote.big',
    '.menu-sec .wrap > *','.contact .narrow > *'];
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1,rootMargin:'0px 0px -6% 0px'});
  var seen=new Set(),count=new Map();
  d.querySelectorAll(SEL.join(',')).forEach(function(el){
    if(seen.has(el)||el.closest('.page-hero,.hero'))return;seen.add(el);
    /* 親の中での順番で、少しずつ時間差をつける（最大4つ目まで） */
    var p=el.parentElement,n=count.get(p)||0;count.set(p,n+1);
    el.setAttribute('data-rv','');el.style.setProperty('--d',Math.min(n,3)*90+'ms');io.observe(el);
  });
})();
