(function(){
  var root=document.documentElement;
  var RSV={ja:'https://www.tablecheck.com/ja/glutenfree/reserve/landing?require_venue=true',
           en:'https://www.tablecheck.com/en/glutenfree/reserve/landing?require_venue=true'};
  /* 日本語ページ・英語ページが別URLのとき（data-lang-fixed）は、URLの言語を使う。ブラウザの言語や保存した言語では切り替えない */
  var fixed=root.getAttribute('data-lang-fixed');
  function setLang(l){
    root.setAttribute('data-lang',l); root.lang=l;
    document.querySelectorAll('a.rsv').forEach(function(a){a.href=RSV[l]});
    document.dispatchEvent(new CustomEvent('langchange',{detail:l}));
    if(!fixed)try{localStorage.setItem('tsk-lang',l)}catch(e){}
  }
  var saved=null; try{saved=localStorage.getItem('tsk-lang')}catch(e){}
  var q=new URLSearchParams(location.search).get('lang');
  setLang(fixed||q||saved||((navigator.language||'ja').toLowerCase().indexOf('ja')===0?'ja':'en'));
  document.querySelectorAll('[data-lang-toggle]').forEach(function(b){b.addEventListener('click',function(){setLang(root.getAttribute('data-lang')==='ja'?'en':'ja')})});
  var tabs=document.querySelectorAll('.store-tabs button'),cards=document.querySelectorAll('.cards .card');
  tabs.forEach(function(t){t.addEventListener('click',function(){var i=+t.dataset.i;
    tabs.forEach(function(x,j){x.setAttribute('aria-selected',j===i)});
    cards.forEach(function(c,j){c.classList.toggle('on',j===i)});});});
  var btn=document.getElementById('menuBtn'),dr=document.getElementById('drawer');
  btn.addEventListener('click',function(){var o=dr.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
  dr.addEventListener('click',function(e){if(e.target.closest('a')){dr.classList.remove('open');btn.setAttribute('aria-expanded','false')}});
})();
