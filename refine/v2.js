/* 改修デモ v2 の追加スクリプト。script.js と anim/site.js の後に読み込む。 */
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* 全要素を動かさず、重要な部分だけにする：小さな要素は動かさず、親の節ごとに現れる */
  if(!reduce){
    document.querySelectorAll('.ig a, .badges li, .awards li, .ticks li, .steps li, .biz > div, .nums > div, .dl-grid > div, .svc-row, .pt, .policy').forEach(function(e){
      e.removeAttribute('data-a');e.style.removeProperty('--d');
    });
  }
  /* 店舗タブ：キーボードの左右キーでも切り替えられる */
  var tabs=document.querySelector('.store-tabs');
  if(tabs){
    tabs.setAttribute('role','tablist');
    tabs.addEventListener('keydown',function(e){
      if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
      var bs=[].slice.call(tabs.querySelectorAll('button')),i=bs.indexOf(document.activeElement);
      if(i<0)return;var n=bs[(i+(e.key==='ArrowRight'?1:bs.length-1))%bs.length];n.focus();n.click();e.preventDefault();
    });
  }
})();
