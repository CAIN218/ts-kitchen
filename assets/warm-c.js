/* 案C 用の小さなJS（3回目）
   - 差し色は 3（金茶）で固定。切り替えの UI はなくした（plan 12）
   - ヘッダーの高さを --hd-h に入れる（固定のドロワーと FV の高さに使う）
   - SP の固定予約ボタンを、店舗欄・コンサルの入口が見えている間は隠す（html に warm-c-stop）
   - ドロワーにヘッダーと同じ SNS を写す
   - お問い合わせ：?type=catering などで「お問い合わせの種類」を選んだ状態にする（plan 13） */
(function(){
  var d=document,r=d.documentElement;
  r.setAttribute('data-acc','3');

  /* ヘッダーの高さ（スクロールで低くなるので ResizeObserver で追う） */
  var hd=d.querySelector('.hd-in')||d.querySelector('.hd');
  function setH(){if(hd)r.style.setProperty('--hd-h',Math.round(hd.getBoundingClientRect().height)+'px')}
  setH();if(hd&&'ResizeObserver' in window)new ResizeObserver(setH).observe(hd);else addEventListener('resize',setH);

  /* 固定予約ボタンを隠す範囲（warm.js の warm-stop に重ねる） */
  if('IntersectionObserver' in window){
    var t=d.querySelectorAll('#stores,.cons-band');
    if(t.length){
      var vis=new Set();
      var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)});r.classList.toggle('warm-c-stop',vis.size>0)},{threshold:0});
      t.forEach(function(el){io.observe(el)});
    }
  }

  /* ドロワーが開いている間、裏のページを止める（overflow:hidden だけでは iPhone で動くため、body を今の位置で固定し、閉じたら同じ位置に戻す） */
  var dr=d.getElementById('drawer'),y=0;
  if(dr&&'MutationObserver' in window){
    new MutationObserver(function(){
      var open=dr.classList.contains('open'),locked=r.classList.contains('warm-c-lock');
      if(open&&!locked){y=window.scrollY;d.body.style.top=(-y)+'px';r.classList.add('warm-c-lock')}
      else if(!open&&locked){r.classList.remove('warm-c-lock');d.body.style.top='';var sb=r.style.scrollBehavior;r.style.scrollBehavior='auto';window.scrollTo(0,y);r.style.scrollBehavior=sb}
    }).observe(dr,{attributes:true,attributeFilter:['class']});
  }

  /* ドロワーにも SNS（リンク先・ラベルは同じ） */
  var f=d.querySelector('.drawer-foot');
  if(f)[].forEach.call(d.querySelectorAll('.hd .tools .sns'),function(a){f.appendChild(a.cloneNode(true))});

  /* 英語の H1：固定の改行を空白に置き換え、text-wrap:balance で均す（1 語だけの行と、語のくっつきを防ぐ。文言は同じ） */
  if((r.getAttribute('lang')||'').indexOf('en')===0){var h1=d.querySelector('.hero-in h1');if(h1)[].forEach.call(h1.querySelectorAll('br'),function(b){b.parentNode.replaceChild(d.createTextNode(' '),b)})}

  /* お問い合わせの種類：URL の ?type= で選ぶ */
  var m=/[?&]type=([a-z]+)/.exec(location.search),sel=d.querySelector('.cf7 select[name=type]');
  if(m&&sel){[].forEach.call(sel.options,function(o){if(o.value===m[1])sel.value=m[1]})}
})();
