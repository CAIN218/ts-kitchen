/* リニューアル（renew）の追加スクリプト。script.js の後に読み込む。動きは最小限。 */
(function(){
  var d=document;
  /* ヘッダー：スクロールで少しコンパクトに */
  var hd=d.querySelector('.hd'),tk=false;
  function upd(){tk=false;if(hd)hd.classList.toggle('scrolled',scrollY>40)}
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd();
  /* いま見ているページを支援技術にも伝える */
  d.querySelectorAll('.nav a.on,.drawer>a.on').forEach(function(a){a.setAttribute('aria-current','page')});
  /* メニュー（ドロワー）：Escで閉じる */
  var btn=d.getElementById('menuBtn'),dr=d.getElementById('drawer');
  if(btn&&dr){
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&dr.classList.contains('open')){dr.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.focus()}});
  }
  /* タブ：矢印キーで移動できる（店舗・メニューの店舗） */
  function tablist(el){
    if(!el)return;el.setAttribute('role','tablist');
    el.querySelectorAll('button').forEach(function(b){b.setAttribute('role','tab')});
    el.addEventListener('keydown',function(e){
      var k=e.key;if(k!=='ArrowRight'&&k!=='ArrowLeft'&&k!=='Home'&&k!=='End')return;
      var bs=[].slice.call(el.querySelectorAll('button')),i=bs.indexOf(d.activeElement);if(i<0)return;
      var n=k==='Home'?0:k==='End'?bs.length-1:(i+(k==='ArrowRight'?1:bs.length-1))%bs.length;
      bs[n].focus();bs[n].click();e.preventDefault();
    });
  }
  tablist(d.querySelector('.store-tabs'));tablist(d.querySelector('.menu-stores'));
  /* メニュー画像が切り替わるとき、やわらかく差し替える */
  var mv=d.querySelector('.menu-view');
  if(mv)d.querySelectorAll('.menu-stores,.menu-cats').forEach(function(g){g.addEventListener('click',function(e){if(!e.target.closest('button'))return;setTimeout(function(){mv.classList.remove('sw');void mv.offsetWidth;mv.classList.add('sw')},0)})});
  /* 画像拡大：開いたら閉じるボタンへ、閉じたら元の位置へ */
  var lb=d.getElementById('lightbox'),link=d.getElementById('menuLink');
  if(lb&&window.MutationObserver){
    new MutationObserver(function(){
      var cb=lb.querySelector('.lb-close');
      if(!lb.hidden){lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','メニュー画像 / Menu image');if(cb)cb.focus()}
      else if(link)link.focus();
    }).observe(lb,{attributes:true,attributeFilter:['hidden']});
  }
})();
