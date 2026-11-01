/* デモ専用：アクセント色の切り替えと「改修前／改修後」の比較（本番には入れない） */
(function(){
  var r=document.documentElement,css=document.getElementById('refreshCss'),bs=document.querySelectorAll('.rf-bar button');
  var q=new URLSearchParams(location.search),acc=q.get('accent')||'orange',before=q.get('before')==='1';
  function paint(){r.setAttribute('data-accent',acc);css.disabled=before;
    bs.forEach(function(b){var on=b.dataset.accent?(!before&&b.dataset.accent===acc):(b.dataset.mode==='before'?before:!before);b.setAttribute('aria-pressed',on)})}
  bs.forEach(function(b){b.addEventListener('click',function(){if(b.dataset.accent){acc=b.dataset.accent;before=false}else before=b.dataset.mode==='before';paint()})});
  paint();
  /* ページを移っても選択を保つ */
  document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href');
    if(/^[\w-]+\.html$/.test(h)||h==='./'){var u=new URL(h,location.href);u.searchParams.set('accent',acc);if(before)u.searchParams.set('before','1');a.href=u.toString()}});
})();
