/* デモ専用：改修前／前回／今回、ファーストビューA案・B案、アクセント色の切り替え（本番には入れない）。切り替えはページを読み直して反映する。 */
(function(){
  var r=document.documentElement,q=new URLSearchParams(location.search),mode=r.getAttribute('data-mode'),acc=r.getAttribute('data-accent'),hero=r.getAttribute('data-hero');
  document.querySelectorAll('.rn-bar [data-mode]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.mode===mode)});
  document.querySelectorAll('.rn-bar [data-hero]').forEach(function(b){b.setAttribute('aria-pressed',mode==='renew2'&&b.dataset.hero===hero)});
  document.querySelectorAll('.rn-bar [data-accent]').forEach(function(b){b.setAttribute('aria-pressed',mode!=='before'&&b.dataset.accent===acc)});
  function go(p){var u=new URL(location.href);Object.keys(p).forEach(function(k){u.searchParams.set(k,p[k])});location.href=u.toString()}
  document.querySelectorAll('.rn-bar [data-mode]').forEach(function(b){b.addEventListener('click',function(){go({mode:b.dataset.mode})})});
  document.querySelectorAll('.rn-bar [data-hero]').forEach(function(b){b.addEventListener('click',function(){go({mode:'renew2',hero:b.dataset.hero})})});
  document.querySelectorAll('.rn-bar [data-accent]').forEach(function(b){b.addEventListener('click',function(){go({mode:mode==='before'?'renew2':mode,accent:b.dataset.accent})})});
  document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href');
    if(/^[\w-]+\.html(#.*)?$/.test(h)||h==='./'){var u=new URL(h,location.href);u.searchParams.set('accent',acc);u.searchParams.set('mode',mode);u.searchParams.set('hero',hero);a.href=u.toString()}});
})();
