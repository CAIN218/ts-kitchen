/* デモ専用（本番には入れない）：改修前／前回／今回、ファーストビュー、アクセント色の切り替え。フォームの入力チェックと「送信中→送信完了」の見た目の確認用。
   フォームの送信先・送信機能は変えていない（本番では Contact Form 7 がこの役目をする）。 */
(function(){
  var r=document.documentElement,mode=r.getAttribute('data-mode'),acc=r.getAttribute('data-accent'),hero=r.getAttribute('data-hero');
  document.querySelectorAll('.rn-bar [data-mode]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.mode===mode)});
  document.querySelectorAll('.rn-bar [data-hero]').forEach(function(b){b.setAttribute('aria-pressed',false)});
  document.querySelectorAll('.rn-bar [data-accent]').forEach(function(b){b.setAttribute('aria-pressed',mode!=='before'&&b.dataset.accent===acc)});
  function go(p){var u=new URL(location.href);Object.keys(p).forEach(function(k){u.searchParams.set(k,p[k])});location.href=u.toString()}
  document.querySelectorAll('.rn-bar [data-mode]').forEach(function(b){b.addEventListener('click',function(){go({mode:b.dataset.mode})})});
  document.querySelectorAll('.rn-bar [data-hero]').forEach(function(b){b.addEventListener('click',function(){go({mode:'renew14'})})});
  document.querySelectorAll('.rn-bar [data-accent]').forEach(function(b){b.addEventListener('click',function(){go({mode:mode==='before'?'renew14':mode,accent:b.dataset.accent})})});
  document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href');
    if(/^[\w-]+\.html(#.*)?$/.test(h)||h==='./'){var u=new URL(h,location.href);u.searchParams.set('accent',acc);u.searchParams.set('mode',mode);u.searchParams.set('hero',hero);a.href=u.toString()}});

  /* ── フォームの見た目確認（デモ） ── */
  var T={req:{ja:'この項目は必須です。',en:'This field is required.'},mail:{ja:'メールアドレスの形式をご確認ください。',en:'Please check the email address.'},
    agree:{ja:'同意が必要です。',en:'Consent is required.'},sending:{ja:'送信中…',en:'Sending…'},ok:{ja:'送信しました。ありがとうございます。（デモ表示）',en:'Sent. Thank you. (demo)'},
    ng:{ja:'入力内容をご確認ください。',en:'Please check the highlighted fields.'}};
  function L(k){return T[k][r.getAttribute('data-lang')==='en'?'en':'ja']}
  document.querySelectorAll('form.cf7.demo').forEach(function(f){
    var btn=f.querySelector('button.btn'),out=null;
    function clear(){f.querySelectorAll('.wpcf7-not-valid-tip').forEach(function(t){t.remove()});f.querySelectorAll('[aria-invalid]').forEach(function(i){i.removeAttribute('aria-invalid')});
      f.querySelectorAll('.not-valid').forEach(function(i){i.classList.remove('not-valid')})}
    function tip(el,key){var t=document.createElement('span');t.className='wpcf7-not-valid-tip';t.setAttribute('role','alert');t.textContent=L(key);
      (el.closest('label')||el.parentNode).appendChild(t);el.setAttribute('aria-invalid','true');el.classList.add('not-valid')}
    f.addEventListener('input',function(e){var t=e.target.closest('label');if(t){var x=t.querySelector('.wpcf7-not-valid-tip');if(x)x.remove();e.target.removeAttribute('aria-invalid');e.target.classList.remove('not-valid')}});
    btn.addEventListener('click',function(){
      if(btn.disabled)return;clear();if(out){out.remove();out=null}
      var bad=[];f.querySelectorAll('label').forEach(function(l){var inp=l.querySelector('input:not([type=checkbox]),textarea');
        if(inp&&l.querySelector('em')&&!inp.value.trim()){tip(inp,'req');bad.push(inp)}
        else if(inp&&inp.type==='email'&&inp.value&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value)){tip(inp,'mail');bad.push(inp)}});
      var cb=f.querySelector('input[type=checkbox]');if(cb&&!cb.checked){tip(cb,'agree');bad.push(cb)}
      out=document.createElement('div');out.className='wpcf7-response-output';out.setAttribute('role','status');
      if(bad.length){out.textContent=L('ng');out.classList.add('ng');btn.parentNode.appendChild(out);bad[0].focus();return}
      f.classList.add('sending');btn.disabled=true;var sp=document.createElement('span');sp.className='wpcf7-spinner';btn.parentNode.appendChild(sp);out.textContent=L('sending');btn.parentNode.appendChild(out);
      setTimeout(function(){sp.remove();f.classList.remove('sending');f.classList.add('sent');out.textContent=L('ok');out.classList.add('ok');btn.disabled=false;f.reset()},1100);
    });
  });
})();
