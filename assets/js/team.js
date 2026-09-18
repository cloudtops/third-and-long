/* Per-team palettes + the picker in the masthead. */
(function(){var T={"bills":{"name":"Buffalo Bills","l":"#00338D","d":"#2476FF","l2":"#C60C30","d2":"#FA0030","tk":"#FF234D","bg":"#00338D","fg":"#F2F3EF","mu":"#94A8C9","ru":"#3A61A5"},"dolphins":{"name":"Miami Dolphins","l":"#007179","d":"#008E97","l2":"#C03A02","d2":"#FC4C02","tk":"#661F02","bg":"#008E97","fg":"#101418","mu":"#10181C","ru":"#047179"},"patriots":{"name":"New England Patriots","l":"#002244","d":"#007CF8","l2":"#C60C30","d2":"#FA0030","tk":"#E5012D","bg":"#002244","fg":"#F2F3EF","mu":"#8C9BA7","ru":"#3A546D"},"jets":{"name":"New York Jets","l":"#125740","d":"#099365","l2":"#125740","d2":"#099365","tk":"#487C6A","bg":"#125740","fg":"#F2F3EF","mu":"#AFC4BB","ru":"#487C6A"},"ravens":{"name":"Baltimore Ravens","l":"#241773","d":"#8068FF","l2":"#826709","d2":"#9E7C0C","tk":"#9E7C0C","bg":"#241773","fg":"#F2F3EF","mu":"#9B97BB","ru":"#554C91"},"bengals":{"name":"Cincinnati Bengals","l":"#C53204","d":"#FB4F14","l2":"#C53204","d2":"#FB4F14","tk":"#C34115","bg":"#FB4F14","fg":"#101418","mu":"#331D17","ru":"#C34115"},"browns":{"name":"Cleveland Browns","l":"#C33000","d":"#FF3C00","l2":"#311D00","d2":"#BD7100","tk":"#311D00","bg":"#FF3C00","fg":"#101418","mu":"#341A14","ru":"#C63206"},"steelers":{"name":"Pittsburgh Steelers","l":"#8F6200","d":"#FFB612","l2":"#8F6200","d2":"#FFB612","tk":"#C68F13","bg":"#FFB612","fg":"#101418","mu":"#5F4916","ru":"#C68F13"},"texans":{"name":"Houston Texans","l":"#03202F","d":"#0089C8","l2":"#A71930","d2":"#FC002B","tk":"#D10D2E","bg":"#03202F","fg":"#F2F3EF","mu":"#8E9A9E","ru":"#3C535D"},"colts":{"name":"Indianapolis Colts","l":"#002C5F","d":"#007CFF","l2":"#002C5F","d2":"#007CFF","tk":"#3A5C82","bg":"#002C5F","fg":"#F2F3EF","mu":"#8C9FB3","ru":"#3A5C82"},"jaguars":{"name":"Jacksonville Jaguars","l":"#006778","d":"#008BA0","l2":"#886617","d2":"#D7A22A","tk":"#DEA82E","bg":"#006778","fg":"#F2F3EF","mu":"#CEDEDD","ru":"#3A8995"},"titans":{"name":"Tennessee Titans","l":"#0C2340","d":"#1678FF","l2":"#236AB1","d2":"#4B92DB","tk":"#4B92DB","bg":"#0C2340","fg":"#F2F3EF","mu":"#919CA6","ru":"#43556A"},"broncos":{"name":"Denver Broncos","l":"#C53204","d":"#FB4F14","l2":"#002244","d2":"#007CF8","tk":"#002244","bg":"#FB4F14","fg":"#101418","mu":"#331D17","ru":"#C34115"},"chiefs":{"name":"Kansas City Chiefs","l":"#D11633","d":"#FB1E41","l2":"#8F6100","d2":"#FFB81C","tk":"#FFBE30","bg":"#DA1735","fg":"#F2F3EF","mu":"#F2F3EF","ru":"#E04C62"},"raiders":{"name":"Las Vegas Raiders","l":"#646B6E","d":"#A5ACAF","l2":"#646B6E","d2":"#A5ACAF","tk":"#81888B","bg":"#A5ACAF","fg":"#101418","mu":"#383D41","ru":"#81888B"},"chargers":{"name":"Los Angeles Chargers","l":"#006BA8","d":"#0087D0","l2":"#8B6600","d2":"#FFC20E","tk":"#453300","bg":"#0087D0","fg":"#101418","mu":"#10171E","ru":"#046BA4"},"bears":{"name":"Chicago Bears","l":"#0B162A","d":"#2878FF","l2":"#BE3503","d2":"#E93F00","tk":"#C83803","bg":"#0B162A","fg":"#F2F3EF","mu":"#91969C","ru":"#424B59"},"lions":{"name":"Detroit Lions","l":"#006FAC","d":"#0084CA","l2":"#006FAC","d2":"#0084CA","tk":"#3A8FBC","bg":"#006FAC","fg":"#F2F3EF","mu":"#EBEFED","ru":"#3A8FBC"},"packers":{"name":"Green Bay Packers","l":"#203731","d":"#339478","l2":"#8F6200","d2":"#FFB612","tk":"#FFB612","bg":"#203731","fg":"#F2F3EF","mu":"#9AA49F","ru":"#52645F"},"vikings":{"name":"Minnesota Vikings","l":"#4F2683","d":"#A256FF","l2":"#846100","d2":"#FFC62F","tk":"#FFC62F","bg":"#4F2683","fg":"#F2F3EF","mu":"#B2A3C5","ru":"#76579D"},"cowboys":{"name":"Dallas Cowboys","l":"#003594","d":"#2B7AFF","l2":"#003594","d2":"#2B7AFF","tk":"#3A63AA","bg":"#003594","fg":"#F2F3EF","mu":"#94A9CC","ru":"#3A63AA"},"giants":{"name":"New York Giants","l":"#0B2265","d":"#4476FF","l2":"#A71930","d2":"#FC002B","tk":"#F20029","bg":"#0B2265","fg":"#F2F3EF","mu":"#919BB5","ru":"#425486"},"eagles":{"name":"Philadelphia Eagles","l":"#004C54","d":"#008B9A","l2":"#004C54","d2":"#008B9A","tk":"#3A7479","bg":"#004C54","fg":"#F2F3EF","mu":"#9BB7B7","ru":"#3A7479"},"commanders":{"name":"Washington Commanders","l":"#5A1414","d":"#FC0000","l2":"#8F6200","d2":"#FFB612","tk":"#FFB612","bg":"#5A1414","fg":"#F2F3EF","mu":"#B29593","ru":"#7E4A49"},"falcons":{"name":"Atlanta Falcons","l":"#A71930","d":"#FC002B","l2":"#A71930","d2":"#FC002B","tk":"#B94D5E","bg":"#A71930","fg":"#F2F3EF","mu":"#E2C5C7","ru":"#B94D5E"},"panthers":{"name":"Carolina Panthers","l":"#0070AC","d":"#0085CA","l2":"#0070AC","d2":"#0085CA","tk":"#046A9F","bg":"#0085CA","fg":"#101418","mu":"#101418","ru":"#046A9F"},"saints":{"name":"New Orleans Saints","l":"#7C6330","d":"#D3BC8D","l2":"#7C6330","d2":"#D3BC8D","tk":"#A49471","bg":"#D3BC8D","fg":"#101418","mu":"#504B3F","ru":"#A49471"},"buccaneers":{"name":"Tampa Bay Buccaneers","l":"#D50A0A","d":"#FD0000","l2":"#AF5100","d2":"#FF7900","tk":"#FFB16E","bg":"#D50A0A","fg":"#F2F3EF","mu":"#F1ECE8","ru":"#DC4241"},"cardinals":{"name":"Arizona Cardinals","l":"#97233F","d":"#F70B45","l2":"#8F6200","d2":"#FFB612","tk":"#FFB612","bg":"#97233F","fg":"#F2F3EF","mu":"#DCC1C5","ru":"#AD5569"},"rams":{"name":"Los Angeles Rams","l":"#003594","d":"#2B7AFF","l2":"#915C00","d2":"#FFA300","tk":"#FFA300","bg":"#003594","fg":"#F2F3EF","mu":"#94A9CC","ru":"#3A63AA"},"49ers":{"name":"San Francisco 49ers","l":"#AA0000","d":"#FF0505","l2":"#7B663B","d2":"#B3995D","tk":"#BFA366","bg":"#AA0000","fg":"#F2F3EF","mu":"#E3C0BD","ru":"#BB3A39"},"seahawks":{"name":"Seattle Seahawks","l":"#002244","d":"#007CF8","l2":"#3C7216","d2":"#69BE28","tk":"#69BE28","bg":"#002244","fg":"#F2F3EF","mu":"#8C9BA7","ru":"#3A546D"}};
var root=document.documentElement,KEY="tal.team",VARS=["--pick","--pick2","--hash-tick","--hero-bg","--hero-fg","--hero-muted","--hero-rule","--hero-accent"];
function isDark(){var a=root.getAttribute("data-theme");
  if(a==="dark")return true; if(a==="light")return false;
  try{return matchMedia("(prefers-color-scheme: dark)").matches}catch(e){return false}}
function read(){try{return localStorage.getItem(KEY)||""}catch(e){return ""}}
function save(v){try{v?localStorage.setItem(KEY,v):localStorage.removeItem(KEY)}catch(e){}}
function label(t){var el=document.getElementById("pickLabel");if(el)el.textContent=t}
function apply(slug){
  var t=T[slug],st=root.style;
  if(!t){VARS.forEach(function(p){st.removeProperty(p)});root.removeAttribute("data-team");label("Pick your team");return}
  st.setProperty("--pick",isDark()?t.d:t.l);
  st.setProperty("--pick2",isDark()?t.d2:t.l2);
  st.setProperty("--hash-tick",t.tk);
  st.setProperty("--hero-bg",t.bg);
  st.setProperty("--hero-fg",t.fg);
  st.setProperty("--hero-muted",t.mu);
  st.setProperty("--hero-rule",t.ru);
  st.setProperty("--hero-accent",t.fg);
  root.setAttribute("data-team",slug);
  label(t.name);
}
apply(read());
try{matchMedia("(prefers-color-scheme: dark)").addEventListener("change",function(){apply(read())})}catch(e){}
function wire(){
  label(T[read()]?T[read()].name:"Pick your team");
  var btn=document.getElementById("pickBtn"),panel=document.getElementById("pickPanel");
  if(!btn||!panel)return;
  function open(v){panel.hidden=!v;btn.setAttribute("aria-expanded",v?"true":"false")}
  btn.addEventListener("click",function(e){e.stopPropagation();open(panel.hidden)});
  panel.addEventListener("click",function(e){
    var b=e.target.closest("button[data-team]");if(!b)return;
    var v=b.getAttribute("data-team");save(v);apply(v);open(false)});
  document.addEventListener("click",function(e){
    if(!panel.hidden&&!panel.contains(e.target)&&e.target!==btn)open(false)});
  document.addEventListener("keydown",function(e){if(e.key==="Escape")open(false)});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",wire);else wire();
})();
