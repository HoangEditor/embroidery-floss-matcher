html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Embroidery Floss Matcher</title>
<meta name="description" content="Find matching embroidery floss colors across DMC, Anchor, Cosmo, J&P Coats.">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;background:#0b0d14;color:#e8eaed;min-height:100vh}
body::before{content:"";position:fixed;inset:0;background:radial-gradient(ellipse 80% 50% at 50% -20%,rgba(99,102,241,.12),transparent),radial-gradient(ellipse 60% 40% at 80% 80%,rgba(168,85,247,.08),transparent);pointer-events:none;z-index:0}
.app{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:40px 20px}
.hero{text-align:center;padding:60px 0 40px;animation:fadeUp .8s}
.hero h1{font-size:2.6rem;font-weight:800;background:linear-gradient(135deg,#fff 30%,#a5b4fc 70%);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{font-size:1.1rem;color:#8b8fa7;margin-top:12px}
.search{background:#151822;border:1px solid #252940;border-radius:14px;padding:6px;display:flex;gap:8px;max-width:500px;margin:0 auto 24px;box-shadow:0 8px 40px rgba(0,0,0,.4);animation:fadeUp .8s .15s both;transition:border-color .3s}
.search:focus-within{border-color:#6366f1;box-shadow:0 8px 40px rgba(99,102,241,.2)}
.search input{flex:1;background:none;border:none;outline:none;font-size:1.1rem;color:#e8eaed;padding:14px 16px;font-family:inherit}
.search input::placeholder{color:#8b8fa7}
.search button{background:#6366f1;color:#fff;border:none;border-radius:10px;padding:14px 24px;font-size:1rem;font-weight:600;cursor:pointer;transition:background .2s}
.search button:hover{background:#5558e6}
.tabs{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:32px;animation:fadeUp .8s .25s both}
.tab{padding:8px 18px;border-radius:99px;border:1px solid #252940;background:#151822;color:#8b8fa7;cursor:pointer;font-size:.88rem;font-weight:500;transition:all .25s}
.tab:hover{border-color:#6366f1;color:#e8eaed}
.tab.on{background:#6366f1;border-color:#6366f1;color:#fff}
.result{display:none;animation:fadeUp .5s}
.result.show{display:block}
.ch{display:flex;gap:24px;align-items:center;padding:28px;background:#151822;border:1px solid #252940;border-radius:14px;margin-bottom:20px;transition:transform .3s,box-shadow .3s}
.ch:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(0,0,0,.3)}
.sw{width:100px;height:100px;border-radius:10px;flex-shrink:0;box-shadow:0 8px 30px rgba(0,0,0,.5);transition:transform .3s}
.ch:hover .sw{transform:scale(1.05)}
.info .code{font-size:2.2rem;font-weight:800}
.info .name{color:#8b8fa7;font-size:1rem}
.info .hex{font-family:monospace;color:#8b8fa7;margin-top:4px}
.conv{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}
.cc{background:#151822;border:1px solid #252940;border-radius:10px;padding:16px;display:flex;align-items:center;gap:12px;transition:all .25s;animation:fadeUp .4s both}
.cc:hover{border-color:#6366f1;transform:translateY(-2px)}
.ccsw{width:40px;height:40px;border-radius:8px}
.ccb{font-size:.75rem;color:#6366f1;font-weight:600;text-transform:uppercase}
.cccode{font-size:1.1rem;font-weight:700}
.sug{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}
.sc{background:#151822;border:1px solid #252940;border-radius:10px;padding:12px;cursor:pointer;display:flex;align-items:center;gap:10px;transition:all .2s;animation:fadeUp .3s both}
.sc:hover{border-color:#6366f1;transform:translateY(-2px)}
.scsw{width:32px;height:32px;border-radius:6px}
.sccode{font-weight:700;font-size:.95rem}
.scname{font-size:.7rem;color:#8b8fa7}
.grid{display:none;grid-template-columns:repeat(auto-fill,minmax(56px,1fr));gap:4px;margin-top:16px}
.gs{aspect-ratio:1;border-radius:6px;cursor:pointer;transition:transform .2s;position:relative}
.gs:hover{transform:scale(1.2);z-index:2;box-shadow:0 6px 20px rgba(0,0,0,.5)}
.gs span{position:absolute;bottom:2px;left:3px;font-size:.52rem;font-weight:700;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.7)}
.footer{text-align:center;padding:40px 0 20px;color:#8b8fa7;font-size:.82rem}
.spin{width:32px;height:32px;border:3px solid #252940;border-top-color:#6366f1;border-radius:50%;animation:sp .6s linear infinite;margin:0 auto 12px}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes sp{to{transform:rotate(360deg)}}
@media(max-width:600px){.hero h1{font-size:1.8rem}.ch{flex-direction:column;text-align:center}.sw{width:80px;height:80px}.conv{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<div class="app">
<header class="hero"><h1>Embroidery Floss Matcher</h1><p>Find matching thread colors across DMC, Anchor, Cosmo &amp; J&amp;P Coats</p></header>
<div class="search"><input id="q" placeholder="Enter DMC code (e.g. 310, 666, 995)..." autofocus onkeydown="if(event.key==='Enter')search()"><button onclick="search()">Match</button></div>
<div class="tabs"><div class="tab on" onclick="filterBrand('all',this)">All Brands</div><div class="tab" onclick="filterBrand('anchor',this)">Anchor</div><div class="tab" onclick="filterBrand('cosmo',this)">Cosmo</div><div class="tab" onclick="filterBrand('jp_coats',this)">J&amp;P Coats</div></div>
<div id="load" style="text-align:center;padding:30px;display:none"><div class="spin"></div></div>
<div class="result" id="r"></div>
<div style="text-align:center;margin-top:40px"><button class="tab" onclick="toggleGrid()" style="padding:10px 24px">All 456 Colors</button></div>
<div class="grid" id="g"></div>
<footer class="footer"><p>456 DMC colors &bull; 449 Cosmo matches &bull; 107 Anchor matches</p></footer>
</div>
<script>
var cur=null,all=[],brand='all';
function search(){
  var q=document.getElementById('q').value.trim();
  if(!q)return;
  var l=document.getElementById('load'),r=document.getElementById('r');
  l.style.display='block';r.classList.remove('show');r.innerHTML='';
  fetch('/api/search?q='+encodeURIComponent(q)).then(function(resp){return resp.json()}).then(function(d){
    l.style.display='none';
    if(d.found){cur=d.color;render(d.color)}
    else if(d.suggestions&&d.suggestions.length){
      var h='<h3 style="margin-bottom:16px">Did you mean...</h3><div class="sug">';
      d.suggestions.forEach(function(c,i){h+='<div class="sc" style="animation-delay:'+(i*.04)+'s" onclick="pick('+JSON.stringify(c.code)+')"><div class="scsw" style="background:'+c.hex+'"></div><div><div class="sccode">'+c.code+'</div><div class="scname">'+c.name+'</div></div></div>'});
      h+='</div>';r.innerHTML=h;r.classList.add('show');
    }else{r.innerHTML='<div style="text-align:center;padding:40px;color:#8b8fa7">No colors found</div>';r.classList.add('show')}
  }).catch(function(e){l.style.display='none';r.innerHTML='<div style="text-align:center;padding:40px;color:#ef4444">Something went wrong. Try again.</div>';r.classList.add('show')});
}
function render(c){
  var conv=[];
  if(c.anchor)conv.push({b:'Anchor',code:c.anchor});
  if(c.cosmo)conv.push({b:'Cosmo',code:c.cosmo});
  if(c.jp_coats)conv.push({b:'J&P Coats',code:c.jp_coats});
  if(brand!=='all')conv=conv.filter(function(x){var b=x.b.toLowerCase().replace(/[ &]/g,'_');return b===brand});
  var h=conv.map(function(x,i){return'<div class="cc" style="animation-delay:'+(.1+i*.08)+'s"><div class="ccsw" style="background:'+c.hex+'"></div><div><div class="ccb">'+x.b+'</div><div class="cccode">#'+x.code+'</div></div></div>'}).join('');
  if(!h)h='<div style="grid-column:1/-1;text-align:center;padding:20px;color:#8b8fa7">No equivalents found</div>';
  var r=document.getElementById('r');
  r.innerHTML='<div class="ch"><div class="sw" style="background:'+c.hex+'"></div><div class="info"><div class="code">DMC '+c.code+'</div><div class="name">'+c.name+'</div><div class="hex">'+c.hex+'</div></div></div><div class="conv">'+h+'</div>';
  r.classList.add('show');r.scrollIntoView({behavior:'smooth',block:'center'});
}
function pick(code){document.getElementById('q').value=code;fetch('/api/color/'+code).then(function(r){return r.json()}).then(function(d){if(d.found){cur=d.color;render(d.color)}})}
function filterBrand(b,el){brand=b;var tabs=document.querySelectorAll('.tab');for(var i=0;i<tabs.length;i++){if(tabs[i]===el)tabs[i].classList.add('on');else tabs[i].classList.remove('on')}if(cur)render(cur)}
function toggleGrid(){
  var g=document.getElementById('g');
  if(g.style.display==='grid'){g.style.display='none';return}
  if(!all.length){g.innerHTML='<div style="text-align:center;padding:40px"><div class="spin"></div></div>';g.style.display='grid';fetch('/api/all?limit=500').then(function(r){return r.json()}).then(function(d){all=d.colors;showGrid()})}
  else showGrid();
}
function showGrid(){
  var g=document.getElementById('g');
  g.innerHTML=all.map(function(c){return'<div class="gs" style="background:'+c.hex+'" onclick="pick('+JSON.stringify(c.code)+')"><span>'+c.code+'</span></div>'}).join('');
  g.style.display='grid';g.scrollIntoView({behavior:'smooth'});
}
document.addEventListener('keydown',function(e){if((e.metaKey||e.ctrlKey)&&e.key==='k'){e.preventDefault();document.getElementById('q').focus()}});
</script>
</body>
</html>"""
with open('/Users/Hoang/Projects/embroidery-floss-matcher/static/index.html','w') as f:
    f.write(html)
print('OK', len(html), 'bytes')
