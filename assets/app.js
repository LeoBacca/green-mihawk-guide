/* ===== Green Mihawk OP17 — script comune ===== */

/* --- salto morbido a un'ancora senza toccare l'hash (l'hash e' del tab) --- */
function jumpTo(id){
  const el = document.getElementById(id);
  if(!el) return;
  el.scrollIntoView({behavior:'smooth', block:'start'});
  document.querySelector('.gtoc')?.classList.remove('open');
}

/* --- tab con hash in URL --- */
function initTabs(){
  document.querySelectorAll('[data-tabs]').forEach(group=>{
    const btns = group.querySelectorAll('.tabs button');
    const panes = document.querySelectorAll('#'+group.dataset.tabs+' > .tabpane');
    function show(name, push){
      btns.forEach(b=>b.classList.toggle('on', b.dataset.tab===name));
      panes.forEach(p=>p.classList.toggle('on', p.dataset.pane===name));
      if(push) history.replaceState(null,'','#'+name);
      if(push){
        const top = group.getBoundingClientRect().top + window.scrollY - 70;
        if(window.scrollY > top) window.scrollTo({top, behavior:'instant'});
      }
      document.dispatchEvent(new CustomEvent('tabshown'));
    }
    btns.forEach(b=>b.addEventListener('click',()=>show(b.dataset.tab,true)));
    const h = decodeURIComponent(location.hash.slice(1));
    const found = [...btns].some(b=>b.dataset.tab===h);
    show(found ? h : btns[0]?.dataset.tab, false);
  });
}

/* --- indice laterale del capitolo aperto, con la voce in lettura evidenziata --- */
let tocObserver = null;
function buildGuideToc(){
  const nav = document.getElementById('gtoc');
  if(!nav) return;
  const pane = document.querySelector('#panes > .tabpane.on') || document.querySelector('.gpage .verb');
  if(!pane) return;
  const heads = [...pane.querySelectorAll('.gs-h h2, .pan > h3, .tl-mark')];
  const title = pane.querySelector('.pane-t')?.textContent || '';
  nav.innerHTML = (title?`<div class="toc-h">${title}</div>`:'') + heads.map(h=>
    `<a href="#${h.id}" data-jump="${h.id}" class="${h.tagName==='H3'?'l3':''}">${h.classList.contains('tl-mark')?'▶ minuto '+h.dataset.m:(h.dataset.t||h.textContent)}</a>`).join('');
  nav.closest('.glayout')?.classList.toggle('notoc', !heads.length);

  tocObserver?.disconnect();
  const links = new Map([...nav.querySelectorAll('a')].map(a=>[a.dataset.jump,a]));
  tocObserver = new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(!e.isIntersecting) return;
      nav.querySelectorAll('a.act').forEach(a=>a.classList.remove('act'));
      const a = links.get(e.target.id);
      if(a){ a.classList.add('act'); if(window.innerWidth>1000) a.scrollIntoView({block:'nearest'}); }
    });
  }, {rootMargin:'-80px 0px -70% 0px'});
  heads.forEach(h=>tocObserver.observe(h));
}
function initGuideToc(){
  if(!document.getElementById('gtoc')) return;
  document.querySelector('.gtoc-b')?.addEventListener('click',()=>
    document.querySelector('.gtoc').classList.toggle('open'));
  document.addEventListener('tabshown', buildGuideToc);
  buildGuideToc();
}

/* --- quiz di mulligan nelle guide: la risposta dell'autore si scopre cliccando --- */
function initMiniQuiz(){
  document.addEventListener('click', e=>{
    const o = e.target.closest('.mq.play .mq-o');
    if(!o) return;
    const q = o.closest('.mq');
    if(q.classList.contains('shown')) return;
    o.classList.add('picked');
    q.classList.add('shown', o.classList.contains('ok') ? 'right' : 'wrong');
  });
}

/* --- tutti i link data-jump (indice, mappa del capitolo) --- */
function initJumps(){
  document.addEventListener('click', e=>{
    const a = e.target.closest('[data-jump]');
    if(!a) return;
    e.preventDefault();
    jumpTo(a.dataset.jump);
  });
}

/* --- indice laterale generico (pagine senza tab) --- */
function initToc(){
  document.querySelectorAll('[data-toc]').forEach(nav=>{
    const src = document.querySelector(nav.dataset.toc);
    if(!src) return;
    let n=0, html='';
    src.querySelectorAll('h2,h3').forEach(h=>{
      if(!h.id) h.id = 'h'+(++n);
      html += `<a href="#${h.id}" class="${h.tagName==='H3'?'h3':''}">${h.textContent}</a>`;
    });
    nav.innerHTML = html;
  });
}

/* --- filtro testuale su elementi con data-search --- */
function initSearch(){
  document.querySelectorAll('[data-searchfor]').forEach(inp=>{
    const items = document.querySelectorAll(inp.dataset.searchfor);
    inp.addEventListener('input',()=>{
      const q = inp.value.trim().toLowerCase();
      items.forEach(el=>{
        el.classList.toggle('hide', q && !el.textContent.toLowerCase().includes(q));
      });
    });
  });
}

/* --- menu: voce corrente, tendine, hamburger --- */
function initNav(){
  const here = location.pathname.split('/').pop() || 'index.html';
  const dir = location.pathname.split('/').slice(-2,-1)[0];
  document.querySelectorAll('nav.main a').forEach(a=>{
    const parts = a.getAttribute('href').split('#')[0].split('/');
    const t = parts.pop();
    const inGuide = parts.includes('guide');
    if(t===here && (inGuide === (dir==='guide'))){
      a.classList.add('on');
      a.closest('.dd')?.classList.add('on');
    }
  });
  const header = document.querySelector('header.top');
  const tog = document.querySelector('.navtoggle');
  tog?.addEventListener('click',()=>{
    const open = document.body.classList.toggle('menu-open');
    tog.setAttribute('aria-expanded', open);
  });
  document.querySelectorAll('.dd-b').forEach(b=>b.addEventListener('click',e=>{
    const dd = b.closest('.dd');
    const was = dd.classList.contains('open');
    document.querySelectorAll('.dd.open').forEach(x=>x.classList.remove('open'));
    dd.classList.toggle('open', !was);
    b.setAttribute('aria-expanded', !was);
    e.stopPropagation();
  }));
  document.addEventListener('click',e=>{
    if(!e.target.closest('.dd')) document.querySelectorAll('.dd.open').forEach(x=>x.classList.remove('open'));
    if(!e.target.closest('header.top')) document.body.classList.remove('menu-open');
  });
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'){ document.querySelectorAll('.dd.open').forEach(x=>x.classList.remove('open'));
      document.body.classList.remove('menu-open'); }
  });
}

document.addEventListener('DOMContentLoaded',()=>{
  initNav(); initTabs(); initToc(); initSearch(); initJumps(); initGuideToc(); initMiniQuiz();
});

/* ===================================================================
   MOTORE QUIZ
   cfg = { steps:[{q, hint, multi, weight(n), opts:[{label, desc, img, none, score:{k:n}}]}],
           results:{ key:{title, tagline, eyebrow, html | html(ctx)} },
           axes:{ key:'Etichetta' },            // per le barre
           afterTop(ctx), after(ctx) -> html    // blocchi extra sopra/sotto al risultato
         }
   Domande multi: ogni opzione scelta somma il suo punteggio moltiplicato per
   weight(n), dove n e' il numero di opzioni scelte. Un'opzione {none:true} e' esclusiva.
   =================================================================== */
function runQuiz(cfg, rootSel){
  const root = document.querySelector(rootSel);
  const chosen = cfg.steps.map(st=>st.multi ? [] : null);

  const bar   = root.querySelector('.qbar i');
  const stage = root.querySelector('.qstage');
  const res   = root.querySelector('.res');

  cfg.steps.forEach((st,si)=>{
    const d = document.createElement('div');
    d.className='qstep'; d.dataset.i=si;
    d.innerHTML = `<h3>${st.q}</h3>${st.hint?`<p class="qhint">${st.hint}</p>`:''}
      ${st.multi?'<span class="qhint-multi">Puoi sceglierne più di uno</span>':''}
      <div class="opts${st.multi?' multi':''}">${st.opts.map((o,oi)=>
        `<button class="opt" data-o="${oi}" type="button" ${st.multi?`aria-pressed="false"`:''}>
           ${st.multi?'<span class="ck">✓</span>':`<span class="k">${String.fromCharCode(65+oi)}</span>`}
           ${o.img?`<img class="oimg" src="${o.img}" alt="" loading="lazy">`:''}
           <span><b>${o.label}</b>${o.desc?`<span>${o.desc}</span>`:''}</span>
         </button>`).join('')}</div>
      <div class="qnav">
        <button class="btn ghost prev" type="button" ${si===0?'style="visibility:hidden"':''}>← Indietro</button>
        <button class="btn next" type="button" disabled>${si===cfg.steps.length-1?'Vedi il risultato':'Avanti →'}</button>
        <span class="qcount">${si+1} / ${cfg.steps.length}</span>
      </div>`;
    stage.appendChild(d);

    const btns = d.querySelectorAll('.opt');
    btns.forEach(b=>b.addEventListener('click',()=>{
      const oi = +b.dataset.o;
      if(st.multi){
        let sel = chosen[si];
        if(st.opts[oi].none) sel = sel.includes(oi) ? [] : [oi];
        else {
          sel = sel.filter(x=>!st.opts[x].none);
          sel = sel.includes(oi) ? sel.filter(x=>x!==oi) : [...sel, oi];
        }
        chosen[si] = sel;
        btns.forEach(x=>{ const on = sel.includes(+x.dataset.o);
          x.classList.toggle('sel', on); x.setAttribute('aria-pressed', on); });
        d.querySelector('.next').disabled = sel.length===0;
      } else {
        btns.forEach(x=>x.classList.remove('sel'));
        b.classList.add('sel');
        chosen[si] = oi;
        d.querySelector('.next').disabled = false;
      }
    }));
    d.querySelector('.next').addEventListener('click',()=>{
      if(si===cfg.steps.length-1) finish(); else go(si+1);
    });
    d.querySelector('.prev')?.addEventListener('click',()=>go(si-1));
  });

  function go(n){
    root.querySelectorAll('.qstep').forEach(s=>s.classList.toggle('on', +s.dataset.i===n));
    bar.style.width = (n/cfg.steps.length*100)+'%';
    res.classList.remove('on');
    stage.classList.remove('hide');
    window.scrollTo({top:root.offsetTop-80, behavior:'smooth'});
  }

  function finish(){
    const score = {};
    const add = (sc,w)=>{ for(const k in sc) score[k] = (score[k]||0) + sc[k]*w; };
    cfg.steps.forEach((st,si)=>{
      if(st.multi){
        const sel = chosen[si].filter(oi=>!st.opts[oi].none);
        const w = st.weight ? st.weight(sel.length) : 1;
        sel.forEach(oi=>add(st.opts[oi].score||{}, w));
      } else {
        const o = st.opts[chosen[si]];
        if(o) add(o.score||{}, 1);
      }
    });
    const keys = Object.keys(cfg.results);
    const max = Math.max(...keys.map(k=>score[k]||0));
    const win = keys.find(k=>(score[k]||0)===max);
    const r = cfg.results[win];
    const ctx = {chosen, score, win, cfg};

    const axes = cfg.axes || cfg.results;
    const tot = Math.max(1, ...Object.values(score));
    const bars = Object.keys(axes).map(k=>{
      const label = typeof axes[k]==='string' ? axes[k] : (axes[k].title||k);
      const v = score[k]||0;
      return `<div class="bar"><span class="t">${label}</span>
        <span class="track"><i data-w="${Math.round(v/tot*100)}"></i></span>
        <span class="v">${Math.round(v*10)/10}</span></div>`;
    }).join('');

    res.innerHTML = `
      <div class="res-head">
        <div class="eyebrow">${r.eyebrow||'Il tuo profilo'}</div>
        <h2>${r.title}</h2>
        <p>${r.tagline}</p>
      </div>
      <div class="bars">${bars}</div>
      ${cfg.afterTop ? cfg.afterTop(ctx) : ''}
      ${typeof r.html==='function' ? r.html(ctx) : r.html}
      ${cfg.after ? cfg.after(ctx) : ''}
      <div class="qnav" style="justify-content:center;margin-top:26px">
        <button class="btn ghost" type="button" onclick="location.reload()">↻ Rifai il quiz</button>
      </div>`;
    stage.classList.add('hide');
    res.classList.add('on');
    bar.style.width='100%';
    requestAnimationFrame(()=>res.querySelectorAll('.bar i').forEach(b=>b.style.width=b.dataset.w+'%'));
    window.scrollTo({top:root.offsetTop-80, behavior:'smooth'});
  }

  go(0);
}
