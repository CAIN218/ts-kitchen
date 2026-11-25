/* 案C 用の小さなJS（3回目・4回目）
   - 差し色は 3（金茶）で固定。切り替えの UI はなくした（plan 12）
   - ヘッダーの高さを --hd-h に入れる（固定のドロワーと FV の高さに使う）
   - 固定予約ボタンの出し入れを1つにまとめる（html に wc-fab。4回目）
   - 背景色と FV のデモの切り替え（4回目）
   - ドロワーにヘッダーと同じ SNS を写す。開いている間は幕（.wc-scrim）と inert（3回目の批評・QA）
   - お問い合わせ：?type=catering などで「お問い合わせの種類」を選んだ状態にする（plan 13） */
(function(){
  var d=document,r=d.documentElement;
  r.setAttribute('data-acc','3');

  /* ヘッダーの高さ（スクロールで低くなるので ResizeObserver で追う） */
  var hd=d.querySelector('.hd-in')||d.querySelector('.hd');
  function setH(){if(hd)r.style.setProperty('--hd-h',Math.round(hd.getBoundingClientRect().height)+'px')}
  setH();if(hd&&'ResizeObserver' in window)new ResizeObserver(setH).observe(hd);else addEventListener('resize',setH);

  /* 固定ボタン（.fab／コンサルは .cta-float）の出し入れ（4回目）：renew14 の fab-on・warm.js の warm-stop・前の warm-c-stop・メニューのスクロール連動アニメの4つをやめ、
     ここだけで html に wc-fab を付け外しする（CSS は opacity と transform の 200ms。display は切り替えない）。
     - 出す：TOP はヒーローを過ぎたら、ほかのページは最初の画面（画面の高さの半分）を過ぎたら
     - 隠す：TOP は #stores とフッターが見えている間。ほかのページは、そのページの予約ボタン・フォームとフッターが見えている間
     - 境目で行ったり来たりしないよう、同じ判定が 120ms 続いたときだけ切り替える */
  var page=d.body.getAttribute('data-page'),fab=d.querySelector('body>.fab,body>.cta-float');
  if(fab){
    var isTop=page==='index',hero=d.querySelector('.hero'),
        stops=[].slice.call(d.querySelectorAll(isTop?'#stores,footer':'.menu-actions,#contact,.cons-hero .cons-cta,footer'));
    var on=false,timer=0,raf=0;
    function want(){
      var vh=window.innerHeight,past=isTop&&hero?hero.getBoundingClientRect().bottom<=0:window.scrollY>vh*.5;
      if(!past)return false;
      for(var i=0;i<stops.length;i++){var b=stops[i].getBoundingClientRect();if(b.top<vh&&b.bottom>0)return false}
      return true;
    }
    function commit(){timer=0;var w=want();if(w!==on){on=w;r.classList.toggle('wc-fab',on)}}
    function check(){raf=0;var w=want();if(w===on){if(timer){clearTimeout(timer);timer=0}return}if(!timer)timer=setTimeout(commit,120)}
    function onScroll(){if(!raf)raf=requestAnimationFrame(check)}
    addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onScroll);
    on=want();r.classList.toggle('wc-fab',on);
  }

  /* ドロワーが開いている間、裏のページを止める（overflow:hidden だけでは iPhone で動くため、body を今の位置で固定し、閉じたら同じ位置に戻す） */
  /* 開いている間は、下に半透明の紺の幕（タップで閉じる）を出し、main・footer・固定ボタンを inert にして Tab が裏へ抜けないようにする */
  var dr=d.getElementById('drawer'),mb=d.getElementById('menuBtn'),y=0,sc=null;
  function behind(on){[].forEach.call(d.querySelectorAll('body>main,body>footer,body>.fab,body>.cta-float,body>.awards-band,body>section'),function(el){on?el.setAttribute('inert',''):el.removeAttribute('inert')})}
  if(dr&&mb){sc=d.createElement('div');sc.className='wc-scrim';sc.setAttribute('aria-hidden','true');d.body.appendChild(sc);
    sc.addEventListener('click',function(){if(dr.classList.contains('open')){dr.classList.remove('open');mb.setAttribute('aria-expanded','false');mb.focus({preventScroll:true})}})}
  if(dr&&'MutationObserver' in window){
    new MutationObserver(function(){
      var open=dr.classList.contains('open'),locked=r.classList.contains('warm-c-lock');
      if(open&&!locked){y=window.scrollY;d.body.style.top=(-y)+'px';r.classList.add('warm-c-lock');behind(true)}
      else if(!open&&locked){behind(false);r.classList.remove('warm-c-lock');d.body.style.top='';var sb=r.style.scrollBehavior;r.style.scrollBehavior='auto';window.scrollTo(0,y);r.style.scrollBehavior=sb}
    }).observe(dr,{attributes:true,attributeFilter:['class']});
  }

  /* ドロワーにも SNS（リンク先・ラベルは同じ） */
  var f=d.querySelector('.drawer-foot');
  if(f)[].forEach.call(d.querySelectorAll('.hd .tools .sns'),function(a){f.appendChild(a.cloneNode(true))});

  /* 英語の H1：固定の改行を空白に置き換え、text-wrap:balance で均す（1 語だけの行と、語のくっつきを防ぐ。文言は同じ） */
  if((r.getAttribute('lang')||'').indexOf('en')===0){var h1=d.querySelector('.hero-in h1');if(h1)[].forEach.call(h1.querySelectorAll('br'),function(b){b.parentNode.replaceChild(d.createTextNode(' '),b)})}

  /* デモ用の切り替え（4回目）：背景色（html[data-bg]）と FV（html[data-fv]、トップだけ）。フッター最下部に置き、選んだものは localStorage に残す。
     最初の値は <head> の小さなスクリプトが ?bg= ?fv= と localStorage から決めている */
  var ft=d.querySelector('footer'),en=(r.getAttribute('lang')||'').indexOf('en')===0;
  function sw(label,key,attr,opts,def){
    var p=d.createElement('p');p.className='acc-switch';p.appendChild(d.createTextNode(label));
    var cur=r.getAttribute(attr)||def;
    opts.forEach(function(o,i){
      if(i)p.appendChild(d.createTextNode(' / '));
      var b=d.createElement('button');b.type='button';b.textContent=o[1];b.setAttribute('aria-pressed',String(o[0]===cur));
      b.addEventListener('click',function(){
        if(o[0]===def)r.removeAttribute(attr);else r.setAttribute(attr,o[0]);
        try{localStorage.setItem(key,o[0])}catch(e){}
        [].forEach.call(p.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',String(x===b))});
        dispatchEvent(new Event('scroll'));
      });
      p.appendChild(b);
    });
    ft.appendChild(p);
  }
  if(ft){
    if(page==='index')sw(en?'Hero: ':'FV：','wc-fv','data-fv',[['0',en?'Current':'今'],['1',en?'1 Card':'1 札'],['2',en?'2 Noren':'2 暖簾'],['3',en?'3 Triptych':'3 三枚組']],'0');
    /* 背景色の切り替えは、B 玄米に決まったのでやめた（yuga 2026-11-25） */
  }

  /* お問い合わせの種類：URL の ?type= で選ぶ */
  var m=/[?&]type=([a-z]+)/.exec(location.search),sel=d.querySelector('.cf7 select[name=type]');
  if(m&&sel){[].forEach.call(sel.options,function(o){if(o.value===m[1])sel.value=m[1]})}
})();
