/* デザイン案のプレビュー用スクリプト：言語切替と「いま営業中？」の表示 */
(function(){
  var root=document.documentElement;
  function setLang(l){root.setAttribute('data-lang',l);root.lang=l;try{localStorage.setItem('tsk-lang',l)}catch(e){}}
  var saved=null;try{saved=localStorage.getItem('tsk-lang')}catch(e){}
  setLang(new URLSearchParams(location.search).get('lang')||saved||((navigator.language||'ja').toLowerCase().indexOf('ja')===0?'ja':'en'));
  document.querySelectorAll('[data-lang-toggle]').forEach(function(b){b.addEventListener('click',function(){setLang(root.getAttribute('data-lang')==='ja'?'en':'ja')})});

  /* 営業時間（お店の案内どおり）。曜日は 0=日 … 6=土 */
  var H={
    harajuku:function(d){if(d===3)return null;return (d===0||d===6)?[[12,22]]:[[12,16],[17,22]]},
    roppongi:function(d){if(d===2)return null;return [[12,16],[17,22]]},
    ueno:function(d){return d===3?[[7,9.5]]:[[7,9.5],[12,16],[17,22]]}
  };
  function fmt(h){var m=Math.round((h%1)*60);return Math.floor(h)+':'+(m<10?'0'+m:m)}
  function two(ja,en){return '<span lang="ja">'+ja+'</span><span lang="en">'+en+'</span>'}
  function status(id,now){
    var d=now.getDay(),t=now.getHours()+now.getMinutes()/60,s=H[id](d);
    if(!s)return {cls:'off',html:two('本日はお休み','Closed today')};
    for(var i=0;i<s.length;i++){
      if(t>=s[i][0]&&t<s[i][1])return {cls:'on',html:two('営業中','Open now')+' <small>'+two(fmt(s[i][1])+'まで','until '+fmt(s[i][1]))+'</small>'};
      if(t<s[i][0])return {cls:'soon',html:two('準備中','Opening soon')+' <small>'+two(fmt(s[i][0])+'から','at '+fmt(s[i][0]))+'</small>'};
    }
    return {cls:'off',html:two('本日の営業は終了','Closed for today')};
  }
  function tick(){
    var now=new Date(new Date().toLocaleString('en-US',{timeZone:'Asia/Tokyo'}));
    document.querySelectorAll('[data-status]').forEach(function(el){var r=status(el.getAttribute('data-status'),now);el.className=(el.getAttribute('data-base')||'')+' st '+r.cls;el.innerHTML=r.html});
  }
  tick();setInterval(tick,60000);
})();
