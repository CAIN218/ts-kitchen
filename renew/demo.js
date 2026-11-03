/* デモ専用：改修前／今回の切り替えとアクセント色（本番には入れない）。切り替えはページを読み直して反映する。 */
(function(){
  var q=new URLSearchParams(location.search),mode=q.get('mode')==='before'?'before':'renew',acc=document.documentElement.getAttribute('data-accent')||'orange';
  document.querySelectorAll('.rn-bar [data-mode]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.mode===mode)});
  document.querySelectorAll('.rn-bar [data-accent]').forEach(function(b){
    b.setAttribute('aria-pressed',mode==='renew'&&b.dataset.accent===acc);
    b.addEventListener('click',function(){var r=document.documentElement;r.setAttribute('data-accent',b.dataset.accent);
      if(mode!=='renew'){var u=new URL(location.href);u.searchParams.set('mode','renew');u.searchParams.set('accent',b.dataset.accent);location.href=u.toString();return}
      document.querySelectorAll('.rn-bar [data-accent]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});acc=b.dataset.accent;
      var u2=new URL(location.href);u2.searchParams.set('accent',acc);history.replaceState(null,'',u2)})});
  document.querySelectorAll('.rn-bar [data-mode]').forEach(function(b){b.addEventListener('click',function(){var u=new URL(location.href);u.searchParams.set('mode',b.dataset.mode);u.searchParams.set('accent',acc);location.href=u.toString()})});
  document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href');
    if(/^[\w-]+\.html(#.*)?$/.test(h)||h==='./'){var u=new URL(h,location.href);u.searchParams.set('accent',acc);u.searchParams.set('mode',mode);a.href=u.toString()}});
})();
