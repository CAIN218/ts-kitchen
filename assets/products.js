/* 商品ページ（warm-c/products/）だけの小さなJS。デモ用の FV 切り替え（A 紺の舞台／B 2商品分割）をフッターの最下部に置く。
   最初の値は <head> の小さなスクリプトが ?fv=a|b と localStorage（wc-pdfv）から決め、html[data-pdfv="b"] を付ける。A が既定（属性なし） */
(function(){
  var d=document,r=d.documentElement,ft=d.querySelector('footer');
  if(!ft)return;
  var en=(r.getAttribute('lang')||'').indexOf('en')===0,cur=r.getAttribute('data-pdfv')||'a';
  var p=d.createElement('p');p.className='acc-switch';p.appendChild(d.createTextNode(en?'Hero (demo): ':'FV（デモ）：'));
  [['a',en?'A Navy stage':'A 紺の舞台'],['b',en?'B Two products':'B 2商品']].forEach(function(o,i){
    if(i)p.appendChild(d.createTextNode(' / '));
    var b=d.createElement('button');b.type='button';b.textContent=o[1];b.setAttribute('aria-pressed',String(o[0]===cur));
    b.addEventListener('click',function(){
      if(o[0]==='a')r.removeAttribute('data-pdfv');else r.setAttribute('data-pdfv',o[0]);
      try{localStorage.setItem('wc-pdfv',o[0])}catch(e){}
      [].forEach.call(p.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',String(x===b))});
      window.scrollTo(0,0);
    });
    p.appendChild(b);
  });
  p.appendChild(d.createTextNode(en?' (C: not built — not enough photos)':'（C は写真が足りないため作っていません）'));
  ft.appendChild(p);
})();
