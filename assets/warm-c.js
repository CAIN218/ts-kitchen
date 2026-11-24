/* 案C 用の小さなJS：差し色 4 候補の切り替え（デモ用）。
   html[data-acc] を変え、localStorage に保存してページを移っても続くようにする。フッター最下部に文字の切り替えを足す */
(function(){
  var r=document.documentElement,K='warm-c-acc',en=(r.getAttribute('lang')||'').indexOf('en')===0,
      names=en?['Soft orange','Door red','Golden brown','Olive']:['整えたオレンジ','扉の赤','金茶','オリーブ'];
  function get(){try{return localStorage.getItem(K)}catch(e){return null}}
  function set(v){try{localStorage.setItem(K,v)}catch(e){}}
  var saved=get();if(/^[1-4]$/.test(saved||''))r.setAttribute('data-acc',saved);
  var ds=document.querySelector('.demo-switch');if(!ds)return;
  var p=document.createElement('p');p.className='acc-switch';p.appendChild(document.createTextNode(en?'Accent: ':'差し色：'));
  names.forEach(function(n,i){
    if(i)p.appendChild(document.createTextNode(en?' / ':'／'));
    var b=document.createElement('button');b.type='button';b.setAttribute('data-v',String(i+1));b.textContent=(i+1)+' '+n;p.appendChild(b);
  });
  function mark(){var v=r.getAttribute('data-acc')||'3';[].forEach.call(p.querySelectorAll('button'),function(b){b.setAttribute('aria-pressed',b.getAttribute('data-v')===v?'true':'false')})}
  p.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var v=b.getAttribute('data-v');r.setAttribute('data-acc',v);set(v);mark()});
  ds.parentNode.insertBefore(p,ds.nextSibling);mark();
})();
/* SP の固定予約ボタンが、店舗欄のキャンセルポリシー（注記）に重ならないよう、また法人向けの入口（.cons-band）と同時に出ないよう、それらが見えている間は html に warm-c-stop を付けて隠す（warm.js の warm-stop に重ねる） */
(function(){
  var d=document,r=d.documentElement;if(!('IntersectionObserver' in window))return;
  var t=d.querySelectorAll('#stores .policy,.cons-band');if(!t.length)return;
  var vis=new Set();
  var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)});r.classList.toggle('warm-c-stop',vis.size>0)},{threshold:0});
  t.forEach(function(el){io.observe(el)});
})();
/* ドロワーにもヘッダーと同じ SNS（Instagram・YouTube）を出す：ヘッダーのリンクを写して .drawer-foot に入れる（文言・リンク先は同じ） */
(function(){
  var f=document.querySelector('.drawer-foot');if(!f)return;
  [].forEach.call(document.querySelectorAll('.hd .tools .sns'),function(a){f.appendChild(a.cloneNode(true))});
})();
