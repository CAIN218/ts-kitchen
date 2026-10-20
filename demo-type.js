(function(){
var F=[];
var P=[['navy','紺×ピンク（今）'],['orange','紺×オレンジ(ボタンの色)'],['orange-d','墨紺×オレンジ'],['sumi','墨紺×朱'],['forest','深緑×小麦'],['wine','ワイン×金'],['cocoa','焦茶×あかね']];
var h=document.documentElement,bar=document.createElement('div');bar.id='dt';
function row(t,L,k){var s=document.createElement('span');s.innerHTML='<b>'+t+'</b>';L.forEach(function(x){var b=document.createElement('button');b.type='button';b.textContent=x[1];b.dataset.v=x[0];b.onclick=function(){h.setAttribute(k,x[0]);sync()};s.appendChild(b)});bar.appendChild(s)}
function sync(){[].forEach.call(bar.querySelectorAll('button'),function(b){var k=F.some(function(x){return x[0]===b.dataset.v})?'data-ft':'data-pl';b.setAttribute('aria-pressed',h.getAttribute(k)===b.dataset.v)})}
row('配色',P,'data-pl');
document.body.appendChild(bar);
var q=new URLSearchParams(location.search);if(q.get('ft'))h.setAttribute('data-ft',q.get('ft'));if(q.get('pl'))h.setAttribute('data-pl',q.get('pl'));
if(!h.getAttribute('data-pl'))h.setAttribute('data-pl','orange');sync();})();
