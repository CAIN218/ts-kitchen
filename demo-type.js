(function(){
var F=[['mincho','明朝（今のまま）'],['oldmincho','古い明朝（やわらかめ）'],['gothic','ゴシック'],['maru','丸ゴシック']];
var P=[['navy','紺×ピンク（今）'],['coral','紺×コーラル'],['gold','紺×小麦ゴールド'],['forest','深緑×コーラル']];
var h=document.documentElement,bar=document.createElement('div');bar.id='dt';
function row(t,L,k){var s=document.createElement('span');s.innerHTML='<b>'+t+'</b>';L.forEach(function(x){var b=document.createElement('button');b.type='button';b.textContent=x[1];b.dataset.v=x[0];b.onclick=function(){h.setAttribute(k,x[0]);sync()};s.appendChild(b)});bar.appendChild(s)}
function sync(){[].forEach.call(bar.querySelectorAll('button'),function(b){var k=F.some(function(x){return x[0]===b.dataset.v})?'data-ft':'data-pl';b.setAttribute('aria-pressed',h.getAttribute(k)===b.dataset.v)})}
row('見出し',F,'data-ft');row('配色',P,'data-pl');
document.body.appendChild(bar);
var q=new URLSearchParams(location.search);if(q.get('ft'))h.setAttribute('data-ft',q.get('ft'));if(q.get('pl'))h.setAttribute('data-pl',q.get('pl'));
sync();})();
