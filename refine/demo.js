/* デモ専用：改修前／前回／今回の切り替えとアクセント色（本番には入れない） */
(function(){
  var r=document.documentElement,v2=document.getElementById('v2Css'),v1=document.getElementById('v1Css'),bs=document.querySelectorAll('.rf-bar button');
  var q=new URLSearchParams(location.search),acc=q.get('accent')||'orange',mode=q.get('mode')||'v2';
  if(!/^(before|v1|v2)$/.test(mode))mode='v2';
  function paint(){r.setAttribute('data-accent',acc);r.setAttribute('data-mode',mode);v2.disabled=mode!=='v2';v1.disabled=mode!=='v1';
    bs.forEach(function(b){var on=b.dataset.accent?(mode!=='before'&&b.dataset.accent===acc):b.dataset.mode===mode;b.setAttribute('aria-pressed',on)})}
  bs.forEach(function(b){b.addEventListener('click',function(){if(b.dataset.accent){acc=b.dataset.accent;if(mode==='before')mode='v2'}else mode=b.dataset.mode;paint()})});
  paint();
  document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href');
    if(/^[\w-]+\.html$/.test(h)||h==='./'){var u=new URL(h,location.href);u.searchParams.set('accent',acc);u.searchParams.set('mode',mode);a.href=u.toString()}});
})();
