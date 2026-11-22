/* RENEW 第6次の追加スクリプト。renew5.js の後に読み込む。 */
(function(){
  var d=document,lb=d.getElementById('lightbox'),link=d.getElementById('menuLink');
  /* メニュー画像の拡大：押した位置を中心に円形に開く／閉じる */
  if(lb&&link){
    link.addEventListener('click',function(e){
      var x=e.clientX||innerWidth/2,y=e.clientY||innerHeight/2;
      lb.style.setProperty('--cx',x+'px');lb.style.setProperty('--cy',y+'px');
    },true);
  }
  /* コンサルの流れ：リングを左から順に描く */
  d.querySelectorAll('.steps li').forEach(function(li,i){li.style.setProperty('--d',i*160+'ms')});
})();
