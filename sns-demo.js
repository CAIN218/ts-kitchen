/* SNS紹介ブロックの動作確認用（プレビュー専用）。YouTubeはクリックで読み込み、Instagramは公式の埋め込みを使う。 */
(function(){
  function ytId(u){var m=(u||'').match(/(?:v=|youtu\.be\/|shorts\/|embed\/)([\w-]{11})/);return m&&m[1]}
  function play(el){var id=el.getAttribute('data-yt');if(!id||el.querySelector('iframe'))return;
    el.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="YouTube"></iframe>'}
  function setYt(id){document.querySelectorAll('[data-yt-box]').forEach(function(el){
    el.setAttribute('data-yt',id);
    el.innerHTML='<img alt="" src="https://i.ytimg.com/vi/'+id+'/hqdefault.jpg"><i class="yt-play"></i>'})}
  function setIg(path){document.querySelectorAll('[data-ig-box]').forEach(function(box){
    box.innerHTML='<blockquote class="instagram-media" data-instgrm-permalink="https://www.'+path+'/" data-instgrm-version="14"></blockquote>';
    if(window.instgrm){instgrm.Embeds.process()}else{var s=document.createElement('script');s.async=true;s.src='https://www.instagram.com/embed.js';document.body.appendChild(s)}})}
  document.querySelectorAll('[data-yt-box]').forEach(function(el){
    el.setAttribute('role','button');el.setAttribute('tabindex','0');
    el.addEventListener('click',function(){play(el)});
    el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();play(el)}})});
  var f=document.getElementById('pvTools');
  if(f)f.addEventListener('submit',function(e){e.preventDefault();
    var y=ytId(f.yt.value),ig=f.ig.value.match(/instagram\.com\/(?:p|reel)\/[\w-]+/);
    if(y)setYt(y);if(ig)setIg(ig[0])});
})();
