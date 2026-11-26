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
  if((r.getAttribute('lang')||'').indexOf('en')===0){var h1=d.querySelector('.hero-in h1');if(h1)[].forEach.call(h1.querySelectorAll('br'),function(b){b.parentNode.insertBefore(d.createTextNode(' '),b);b.className='en-br'})}
  /* ↑ 7回目：br は消さずに空白を前に足し、CSS で隠す（.en-br）。FV4・5 の PC だけ、元の改行（2行）を見せる */

  /* デモ用の切り替え（4回目。7回目に 4〜6 へ入れ替え。旧1〜3 は ?fv=1〜3 で開ける）：背景色（html[data-bg]）と FV（html[data-fv]、トップだけ）。フッター最下部に置き、選んだものは localStorage に残す。
     最初の値は <head> の小さなスクリプトが ?bg= ?fv= と localStorage から決めている */
  var ft=d.querySelector('footer'),en=(r.getAttribute('lang')||'').indexOf('en')===0;
  function sw(label,key,attr,opts,def){
    var p=d.createElement('p');p.className='acc-switch';p.appendChild(d.createTextNode(label));
    var cur=r.getAttribute(attr)||def;
    opts.forEach(function(o,i){
      if(i)p.appendChild(d.createTextNode(' / '));
      var b=d.createElement('button');b.type='button';b.textContent=o[1];b.setAttribute('aria-pressed',String(o[0]===cur));
      b.addEventListener('click',function(){
        if(o[0]===def&&attr!=='data-fv')r.removeAttribute(attr);else r.setAttribute(attr,o[0]);
        try{localStorage.setItem(key,o[0])}catch(e){}
        [].forEach.call(p.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',String(x===b))});
        dispatchEvent(new Event('scroll'));
      });
      p.appendChild(b);
    });
    ft.appendChild(p);
  }
  if(ft){
    /* FV は「全画面の写真からふわっと」に決定したので、切り替えはやめた（yuga 2026-11-25） */
    /* 背景色の切り替えは、B 玄米に決まったのでやめた（yuga 2026-11-25） */
  }

  /* お問い合わせの種類：URL の ?type= で選ぶ */
  var m=/[?&]type=([a-z]+)/.exec(location.search),sel=d.querySelector('.cf7 select[name=type]');
  if(m&&sel){[].forEach.call(sel.options,function(o){if(o.value===m[1])sel.value=m[1]})}
})();
/* 13回目：お問い合わせを3段階に（入力 → 確認 → 送信・完了）。デモなので、どこにも送らない。本番は Contact Form 7 の確認画面のしくみに置き換える */
(function(){
  var d=document,f=d.querySelector('form.cf7.wc3');if(!f)return;
  var en=(d.documentElement.getAttribute('lang')||'').indexOf('en')===0,L=function(j,e){return en?e:j};
  var body=f.parentNode,steps=d.querySelectorAll('.wc-steps li'),sec=f.closest('section')||body;
  /* GDPR：開いて読める */
  var g=f.querySelector('.gdpr-open'),gt=d.getElementById('gdpr-txt');
  if(g&&gt)g.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();var o=gt.hidden;gt.hidden=!o;g.setAttribute('aria-expanded',o?'true':'false')});
  function step(n){[].forEach.call(steps,function(li){var k=+li.getAttribute('data-s');li.classList.toggle('done',k<n);if(k===n)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current')});
    body.setAttribute('data-step',n);var top=sec.getBoundingClientRect().top+window.scrollY-(parseInt(getComputedStyle(d.documentElement).getPropertyValue('--hd-h'))||64)-8;
    if(window.scrollY>top)window.scrollTo({top:top,behavior:'smooth'})}
  function clear(){[].forEach.call(f.querySelectorAll('.wpcf7-not-valid-tip,.wpcf7-response-output'),function(t){t.remove()});[].forEach.call(f.querySelectorAll('.not-valid'),function(i){i.classList.remove('not-valid');i.removeAttribute('aria-invalid')})}
  function tip(el,msg){var t=d.createElement('span');t.className='wpcf7-not-valid-tip';t.setAttribute('role','alert');t.textContent=msg;(el.closest('label')||el.parentNode).appendChild(t);el.classList.add('not-valid');el.setAttribute('aria-invalid','true')}
  f.addEventListener('input',function(e){var l=e.target.closest('label');if(l){var x=l.querySelector('.wpcf7-not-valid-tip');if(x)x.remove();e.target.classList.remove('not-valid');e.target.removeAttribute('aria-invalid')}});
  f.addEventListener('change',function(e){f.dispatchEvent(new Event('input'));var l=e.target.closest('label');if(l){var x=l.querySelector('.wpcf7-not-valid-tip');if(x)x.remove();e.target.classList.remove('not-valid')}});
  function rows(){var out=[];[].forEach.call(f.querySelectorAll('p>label'),function(l){var el=l.querySelector('select,input:not([type=checkbox]),textarea');if(!el)return;var name=l.querySelector('span').textContent;
    var v=el.tagName==='SELECT'?(el.value?el.options[el.selectedIndex].text:''):el.value.trim();out.push([name,v])});return out}
  f.querySelector('.wc3-next').addEventListener('click',function(){
    clear();var bad=[];
    [].forEach.call(f.querySelectorAll('p>label'),function(l){var el=l.querySelector('select,input:not([type=checkbox]),textarea');if(!el)return;var req=!!l.querySelector('em');
      if(el.tagName==='SELECT'){if(!el.value){tip(el,L('お問い合わせの種類を選んでください。','Please choose a type of inquiry.'));bad.push(el)}}
      else if(req&&!el.value.trim()){tip(el,L('この項目は必須です。','This field is required.'));bad.push(el)}
      else if(el.type==='email'&&el.value&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value)){tip(el,L('メールアドレスの形式をご確認ください。','Please check the email address.'));bad.push(el)}});
    var cb=f.querySelector('input[type=checkbox]');if(cb&&!cb.checked){tip(cb,L('同意が必要です。','Consent is required.'));bad.push(cb)}
    if(bad.length){var o=d.createElement('div');o.className='wpcf7-response-output ng';o.setAttribute('role','alert');o.textContent=L('入力内容をご確認ください。','Please check the highlighted fields.');this.parentNode.appendChild(o);bad[0].focus();return}
    var c=body.querySelector('.wc3-confirm');if(c)c.remove();c=d.createElement('div');c.className='wc3-confirm';
    var h='<h2 tabindex="-1">'+L('入力内容の確認','Review your message')+'</h2><p class="wc3-lead">'+L('以下の内容でよろしければ「送信する」を押してください。','If everything looks right, press “Send”.')+'</p><dl>';
    rows().forEach(function(r){var v=r[1]?r[1].replace(/[&<>"]/g,function(m){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]}):'<span class="none">'+L('（未入力）','(not provided)')+'</span>';h+='<dt>'+r[0]+'</dt><dd>'+v+'</dd>'});
    h+='<dt>GDPR</dt><dd>'+L('同意する','Agreed')+'</dd></dl><p class="wc3-acts"><button type="button" class="btn line wc3-back">'+L('入力画面に戻る','Back to edit')+'</button><button type="button" class="btn wc3-send">'+L('送信する','Send')+'</button></p>';
    c.innerHTML=h;body.appendChild(c);step(2);c.querySelector('h2').focus({preventScroll:true});
    c.querySelector('.wc3-back').addEventListener('click',function(){c.remove();step(1);f.querySelector('.wc3-next').focus({preventScroll:true})});
    c.querySelector('.wc3-send').addEventListener('click',function(){var b=this;b.disabled=true;b.classList.add('sending');b.firstChild&&(b.textContent=L('送信中…','Sending…'));
      setTimeout(function(){c.remove();f.reset();var dn=d.createElement('div');dn.className='wc3-done';
        dn.innerHTML='<h2 tabindex="-1">'+L('送信が完了しました','Your message has been sent')+'</h2><p>'+L('お問い合わせありがとうございます。内容を確認のうえ、ご連絡いたします。','Thank you for contacting us. We will get back to you after reviewing your message.')+'</p><p class="wc3-demo">'+L('※ これはデモです。実際には送信されていません。','* This is a demo. Nothing was actually sent.')+'</p>';
        body.appendChild(dn);step(3);dn.querySelector('h2').focus({preventScroll:true})},900)})
  });
})();
/* 13回目：FV の帯とヘッダーは、写真の表示と文字の読み込みが済んでから動かす（途中で読み込みが重なると、がくっと止まるため）。最大 1.2 秒待つ */
(function(){var r=document.documentElement;if(r.getAttribute('data-fv')!=='8'||!document.querySelector('.fv8-panel'))return;r.classList.add('fv-wait');
  var done=false,go=function(){if(done)return;done=true;requestAnimationFrame(function(){r.classList.remove('fv-wait')})};
  var im=document.querySelector('.fvx-band img'),ps=[];if(im&&im.decode)ps.push(im.decode().catch(function(){}));if(document.fonts&&document.fonts.ready)ps.push(document.fonts.ready);
  Promise.all(ps).then(go);setTimeout(go,1200)})();

/* 16回目（yuga 2026-11-25「受賞歴のアニメーションの線がない」）：renew14.js は最初の年表（沿革）だけに線を引く。2つ目以降（会社概要の受賞歴）にも同じ線と表示の流れを付ける */
(function(){
  var d=document,tls=[].slice.call(d.querySelectorAll('.timeline')).slice(1);if(!tls.length)return;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  tls.forEach(function(tl){
    var lis=[].slice.call(tl.children);
    lis.forEach(function(li,i){li.removeAttribute('data-rv');li.classList.remove('in');li.style.setProperty('--i',i)});
    function mark(){lis.forEach(function(li){var t=li.querySelector('time');if(!t)return;
      var fs=parseFloat(getComputedStyle(t).fontSize),m=parseFloat(getComputedStyle(t,'::before').height)||11;
      li.style.setProperty('--mk',(t.getBoundingClientRect().top-li.getBoundingClientRect().top+fs*.62+m/2)+'px')})}
    mark();var mw=innerWidth;addEventListener('resize',function(){if(innerWidth!==mw){mw=innerWidth;mark()}});d.addEventListener('langchange',function(){setTimeout(mark,0)});if(d.fonts&&d.fonts.ready)d.fonts.ready.then(mark);
    tl.classList.add('tl-line');
    if(reduce||!('IntersectionObserver' in window)){tl.classList.add('tl-done');return}
    tl.classList.add('tl-wait');
    var io=new IntersectionObserver(function(es){var e=es[0];
      if(e.isIntersecting||e.boundingClientRect.top<0){tl.classList.add('tl-go');io.disconnect();
        setTimeout(function(){tl.classList.add('tl-done')},lis.length*240+1200)}
    },{threshold:0,rootMargin:'0px 0px -12% 0px'});
    io.observe(tl);
  });
})();

/* 18回目（yuga 2026-11-25「メニューのズーム機能をもっと使いやすく」）：メニュー画像の拡大ビューアー。
   ピンチ・ダブルタップ（ダブルクリック）・ホイールで拡大、ドラッグで移動、＋／−／全体ボタン、Esc で閉じる。元の lightbox の代わりに開く */
(function(){
  var d=document,link=d.getElementById('menuLink'),src=d.getElementById('menuImg');if(!link||!src)return;
  var en=(d.documentElement.getAttribute('lang')||'').indexOf('en')===0,L=function(j,e){return en?e:j};
  var v=d.createElement('div');v.className='wc-zoom';v.hidden=true;v.setAttribute('role','dialog');v.setAttribute('aria-modal','true');v.setAttribute('aria-label',L('メニュー画像','Menu image'));
  v.innerHTML='<div class="wz-stage"><img alt="" draggable="false"></div>'+
    '<div class="wz-bar"><button type="button" class="wz-out" aria-label="'+L('縮小','Zoom out')+'">−</button><button type="button" class="wz-fit">'+L('全体','Fit')+'</button><button type="button" class="wz-in" aria-label="'+L('拡大','Zoom in')+'">＋</button></div>'+
    '<button type="button" class="wz-close" aria-label="'+L('閉じる','Close')+'">✕</button>'+
    '<p class="wz-hint">'+L('ピンチ・ダブルタップで拡大、ドラッグで移動','Pinch or double-tap to zoom, drag to move')+'</p>';
  d.body.appendChild(v);
  var stage=v.querySelector('.wz-stage'),im=stage.querySelector('img'),s=1,x=0,y=0,MAX=5,last=null,opener=null;
  function base(){var sw=stage.clientWidth,sh=stage.clientHeight,r=Math.min(sw/im.naturalWidth,sh/im.naturalHeight);return {w:im.naturalWidth*r,h:im.naturalHeight*r,sw:sw,sh:sh}}
  function clamp(){var b=base(),mx=Math.max(0,(b.w*s-b.sw)/2),my=Math.max(0,(b.h*s-b.sh)/2);x=Math.min(mx,Math.max(-mx,x));y=Math.min(my,Math.max(-my,y))}
  function apply(anim){clamp();im.style.transition=anim?'transform .28s cubic-bezier(.2,.7,.2,1)':'none';im.style.transform='translate('+x+'px,'+y+'px) scale('+s+')';v.classList.toggle('zoomed',s>1.01);
    var bi=v.querySelector('.wz-in'),bo=v.querySelector('.wz-out'),bf=v.querySelector('.wz-fit');if(bi){bi.disabled=s>=MAX-.01;bo.disabled=s<=1.01;bf.disabled=s<=1.01}}
  /* 画面上の点 (cx,cy) を中心に倍率を変える */
  function zoomAt(ns,cx,cy,anim){ns=Math.min(MAX,Math.max(1,ns));var r=stage.getBoundingClientRect(),px=cx-r.left-r.width/2,py=cy-r.top-r.height/2;
    x=px-(px-x)*ns/s;y=py-(py-y)*ns/s;s=ns;apply(anim)}
  function center(){var r=stage.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}
  function open(){opener=d.activeElement;im.src=src.currentSrc||src.src;im.alt=src.alt;s=1;x=0;y=0;apply(false);v.hidden=false;d.documentElement.classList.add('wz-open');v.querySelector('.wz-close').focus();
    setTimeout(function(){v.classList.add('hint-off')},2600)}
  function close(){v.hidden=true;v.classList.remove('hint-off');d.documentElement.classList.remove('wz-open');if(opener&&opener.focus)opener.focus()}
  addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#menuLink')){e.preventDefault();e.stopImmediatePropagation();open()}},true);
  v.querySelector('.wz-close').addEventListener('click',close);
  /* 19回目（yuga「プラスボタンでズームすると詰むことがある」）：ボタンを続けて押した時に、ブラウザ自体の拡大（ダブルタップ・ピンチ）が起きて、画面が固まったように見えていた。
     ビューアーの中ではブラウザの拡大を止め、＋−は上限・下限で押せなくし、「全体」でいつでも元に戻せるようにする */
  ['gesturestart','gesturechange','gestureend'].forEach(function(t){d.addEventListener(t,function(e){if(!v.hidden)e.preventDefault()},{passive:false})});
  v.addEventListener('touchend',function(e){if(e.target.closest('button')){e.preventDefault();e.target.closest('button').click()}},{passive:false});
  v.addEventListener('touchmove',function(e){if(e.touches.length>1||!e.target.closest('.wz-stage'))e.preventDefault()},{passive:false});
  v.querySelector('.wz-in').addEventListener('click',function(){var c=center();zoomAt(s*1.6,c[0],c[1],true)});
  v.querySelector('.wz-out').addEventListener('click',function(){var c=center();zoomAt(s/1.6,c[0],c[1],true)});
  v.querySelector('.wz-fit').addEventListener('click',function(){s=1;x=0;y=0;apply(true)});
  d.addEventListener('keydown',function(e){if(v.hidden)return;var c=center();
    if(e.key==='Escape')close();else if(e.key==='+'||e.key==='=')zoomAt(s*1.6,c[0],c[1],true);else if(e.key==='-')zoomAt(s/1.6,c[0],c[1],true);
    else if(/^Arrow/.test(e.key)){e.preventDefault();var k=60;if(e.key==='ArrowLeft')x+=k;if(e.key==='ArrowRight')x-=k;if(e.key==='ArrowUp')y+=k;if(e.key==='ArrowDown')y-=k;apply(true)}
    else if(e.key==='Tab'){var f=[].slice.call(v.querySelectorAll('button')),i=f.indexOf(d.activeElement);e.preventDefault();f[(i+(e.shiftKey?f.length-1:1))%f.length].focus()}});
  stage.addEventListener('wheel',function(e){e.preventDefault();zoomAt(s*Math.exp(-e.deltaY*.0022),e.clientX,e.clientY,false)},{passive:false});
  /* ポインター：1本でドラッグ、2本でピンチ、素早く2回でダブルタップ */
  var pts={},start=null,tap=0,moved=false;
  stage.addEventListener('pointerdown',function(e){stage.setPointerCapture(e.pointerId);pts[e.pointerId]=[e.clientX,e.clientY];moved=false;
    var ids=Object.keys(pts);if(ids.length===2){var a=pts[ids[0]],b=pts[ids[1]];start={dist:Math.hypot(a[0]-b[0],a[1]-b[1]),s:s}}else start=null});
  stage.addEventListener('pointermove',function(e){if(!pts[e.pointerId])return;var p=pts[e.pointerId],dx=e.clientX-p[0],dy=e.clientY-p[1];pts[e.pointerId]=[e.clientX,e.clientY];
    var ids=Object.keys(pts);if(Math.abs(dx)+Math.abs(dy)>2)moved=true;
    if(ids.length===2&&start){var a=pts[ids[0]],b=pts[ids[1]],dist=Math.hypot(a[0]-b[0],a[1]-b[1]);zoomAt(start.s*dist/start.dist,(a[0]+b[0])/2,(a[1]+b[1])/2,false)}
    else if(ids.length===1&&s>1){x+=dx;y+=dy;apply(false)}});
  function up(e){var was=Object.keys(pts).length;delete pts[e.pointerId];if(Object.keys(pts).length<2)start=null;
    if(was===1&&!moved){var now=Date.now();if(now-tap<320){zoomAt(s>1.01?1:2.5,e.clientX,e.clientY,true);tap=0}else tap=now}}
  stage.addEventListener('pointerup',up);stage.addEventListener('pointercancel',up);
  addEventListener('resize',function(){if(!v.hidden)apply(false)});
})();

/* 18回目：写真の原寸への差し替え（data-hq）。原寸が読めた時だけ入れ替え、読めなければ今の画像のまま */
(function(){
  [].forEach.call(document.querySelectorAll('[data-hq]'),function(el){
    var u=el.getAttribute('data-hq'),t=new Image();t.decoding='async';
    t.onload=function(){if(el.tagName==='IMG'){el.removeAttribute('srcset');el.src=u}else el.style.backgroundImage='url("'+u+'")'};
    t.src=u;
  });
})();

/* 「私たちのレストランについて」の店舗写真カルーセル（18回目、20回目に作り直し）
   写真の下に小さな丸（今の写真は塗り）。指でスワイプ、丸を押す、← → キー。4.5秒ごとに自動で次へ、最後の次は最初へ。
   送りはなめらかに（自前のイージングで動かし、その間だけ scroll-snap を外す）。触っている間・操作の直後・画面外・タブが裏の時は止める */
(function(){
  var d=document,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  [].forEach.call(d.querySelectorAll('.wc-car'),function(car){
    var tr=car.querySelector('.car-track'),dots=car.querySelector('.car-dots'),en=(d.documentElement.getAttribute('lang')||'').indexOf('en')===0;
    function slides(){return [].slice.call(tr.querySelectorAll('.car-s'))}
    function build(){dots.innerHTML='';slides().forEach(function(s,k){var b=d.createElement('button');b.type='button';b.className='car-dot';
      b.setAttribute('aria-label',en?('Photo '+(k+1)):((k+1)+'枚目の写真'));b.addEventListener('click',function(){pauseFor(8000);go(k)});dots.appendChild(b)});upd()}
    [].forEach.call(tr.querySelectorAll('img[data-car-img]'),function(im){
      function bad(){var f=im.closest('.car-s');if(f&&slides().length>1){f.remove();build()}}
      if(im.complete&&im.naturalWidth===0&&im.getAttribute('src'))bad();else im.addEventListener('error',bad);
    });
    function pos(s){return Math.max(0,Math.min(s.offsetLeft-(tr.clientWidth-s.offsetWidth)/2,tr.scrollWidth-tr.clientWidth))}
    function idx(){var ss=slides(),sl=tr.scrollLeft;var b=0,bd=1e9;ss.forEach(function(s,k){var dd=Math.abs(pos(s)-sl);if(dd<bd){bd=dd;b=k}});return b}
    function upd(){var i=idx();[].forEach.call(dots.children,function(b,k){if(k===i)b.setAttribute('aria-current','true');else b.removeAttribute('aria-current')});
      slides().forEach(function(s,k){s.toggleAttribute('inert',k!==i)})}
    var anim=null;
    function go(i){var ss=slides();if(!ss.length)return;i=(i+ss.length)%ss.length;var to=pos(ss[i]),from=tr.scrollLeft;
      if(anim)cancelAnimationFrame(anim);if(reduce||Math.abs(to-from)<1){tr.scrollLeft=to;upd();return}
      var t0=null,dur=Math.min(1100,700+Math.abs(to-from)*.5);tr.style.scrollSnapType='none';
      function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
      function step(ts){if(t0===null)t0=ts;var k=Math.min(1,(ts-t0)/dur);tr.scrollLeft=from+(to-from)*ease(k);if(k<1)anim=requestAnimationFrame(step);else{anim=null;tr.style.scrollSnapType='';upd()}}
      anim=requestAnimationFrame(step)}
    tr.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();pauseFor(8000);go(idx()+1)}else if(e.key==='ArrowLeft'){e.preventDefault();pauseFor(8000);go(idx()-1)}});
    var to;tr.addEventListener('scroll',function(){if(anim)return;clearTimeout(to);to=setTimeout(upd,60)},{passive:true});
    addEventListener('resize',function(){tr.scrollLeft=pos(slides()[idx()])});
    var hold=false,seen=false,resume=0;function pauseFor(ms){resume=Date.now()+ms}
    if(!reduce){setInterval(function(){if(hold||!seen||d.hidden||Date.now()<resume||anim)return;go(idx()+1)},4500);
      if('IntersectionObserver' in window)new IntersectionObserver(function(es){seen=es[0].isIntersecting},{threshold:.4}).observe(car);else seen=true;
      car.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')hold=true});car.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse')hold=false});
      tr.addEventListener('focusin',function(){hold=true});tr.addEventListener('focusout',function(){hold=false});
      tr.addEventListener('touchstart',function(){pauseFor(8000);if(anim){cancelAnimationFrame(anim);anim=null;tr.style.scrollSnapType=''}},{passive:true});}
    build();
  });
})();

/* 21b回目（yuga 2026-11-26：ロックはやめる）：ファーストビューの動き（2秒）の途中でスクロール・スワイプ・ホイール・キー操作があったら、
   動きをすぐ終わらせて写真・帯・文字・ヘッダーを最後の状態で出し、そのまま普通にスクロールさせる（操作は止めない） */
(function(){
  var d=document,r=d.documentElement;if(r.getAttribute('data-fv')!=='8'||!d.querySelector('.fv8-panel'))return;
  var evs=['wheel','touchstart','keydown','scroll'],done=false;
  function off(){evs.forEach(function(t){removeEventListener(t,skip,true)})}
  function skip(e){if(done)return;if(e&&e.type==='keydown'&&/^(Tab|Shift|Control|Alt|Meta)$/.test(e.key))return;done=true;off();
    r.classList.remove('fv-wait');
    [].forEach.call(d.querySelectorAll('.fvx-band img,.fv8-panel,body[data-page="index"] .hd'),function(el){
      if(el.getAnimations)el.getAnimations().forEach(function(a){try{a.finish()}catch(_){}})});}
  evs.forEach(function(t){addEventListener(t,skip,{capture:true,passive:true})});
  setTimeout(function(){done=true;off()},6000);
})();
