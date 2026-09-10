/* Highlights the current section in the sticky nav while you scroll. */
(function(){
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a'));
  var map = {};
  var targets = [];
  links.forEach(function(a){
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if(el){ map[el.id] = a; targets.push(el); }
  });
  if(!('IntersectionObserver' in window) || !targets.length) return;

  var visible = {};
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ visible[e.target.id] = e.isIntersecting; });
    var current = null;
    for(var i=0;i<targets.length;i++){
      if(visible[targets[i].id]){ current = targets[i].id; break; }
    }
    links.forEach(function(a){ a.classList.remove('on'); });
    if(current && map[current]) map[current].classList.add('on');
  }, { rootMargin: '-25% 0px -60% 0px', threshold: 0 });

  targets.forEach(function(t){ io.observe(t); });
})();
