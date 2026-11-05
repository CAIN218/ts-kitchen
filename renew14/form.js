/* プレビュー用のフォーム確認：入力チェックと「送信中→送信完了」の見た目だけ（送信はしない）。
   本番では Contact Form 7 がこの役目をするので、WordPress には入れない。 */
(function(){
  var r=document.documentElement;
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
