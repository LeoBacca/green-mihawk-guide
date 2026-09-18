/* ===== Green Mihawk OP17 — script comune ===== */

/* --- tab con hash in URL --- */
function initTabs(){
  document.querySelectorAll('[data-tabs]').forEach(group=>{
    const btns = group.querySelectorAll('.tabs button');
    const panes = document.querySelectorAll('#'+group.dataset.tabs+' > .tabpane');
    function show(name, push){
      btns.forEach(b=>b.classList.toggle('on', b.dataset.tab===name));
      panes.forEach(p=>p.classList.toggle('on', p.dataset.pane===name));
      if(push) history.replaceState(null,'','#'+name);
      window.scrollTo({top:0,behavior:'instant'});
    }
    btns.forEach(b=>b.addEventListener('click',()=>show(b.dataset.tab,true)));
    const h = decodeURIComponent(location.hash.slice(1));
    const found = [...btns].some(b=>b.dataset.tab===h);
    show(found ? h : btns[0]?.dataset.tab, false);
  });
}

/* --- indice laterale generato dagli heading --- */
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

/* --- evidenzia la voce di menu corrente --- */
function initNav(){
  const here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav.main a').forEach(a=>{
    const t = a.getAttribute('href').split('/').pop().split('#')[0];
    if(t===here) a.classList.add('on');
  });
}

document.addEventListener('DOMContentLoaded',()=>{
  initTabs(); initToc(); initSearch(); initNav();
});

/* ===================================================================
   MOTORE QUIZ
   cfg = { steps:[{q,hint,opts:[{label,desc,score:{k:n}}], multi:false}],
           results:{ key:{title,tagline,html} },
           axes:{ key:'Etichetta' }        // per le barre
         }
   =================================================================== */
function runQuiz(cfg, rootSel){
  const root = document.querySelector(rootSel);
  const chosen = cfg.steps.map(()=>null);
  let i = 0;

  const bar   = root.querySelector('.qbar i');
  const stage = root.querySelector('.qstage');
  const res   = root.querySelector('.res');

  cfg.steps.forEach((st,si)=>{
    const d = document.createElement('div');
    d.className='qstep'; d.dataset.i=si;
    d.innerHTML = `<h3>${st.q}</h3>${st.hint?`<p class="qhint">${st.hint}</p>`:''}
      <div class="opts">${st.opts.map((o,oi)=>
        `<button class="opt" data-o="${oi}">
           <span class="k">${String.fromCharCode(65+oi)}</span>
           <span><b>${o.label}</b>${o.desc?`<span>${o.desc}</span>`:''}</span>
         </button>`).join('')}</div>
      <div class="qnav">
        <button class="btn ghost prev" ${si===0?'style="visibility:hidden"':''}>← Indietro</button>
        <button class="btn next" disabled>${si===cfg.steps.length-1?'Vedi il risultato':'Avanti →'}</button>
        <span class="qcount">${si+1} / ${cfg.steps.length}</span>
      </div>`;
    stage.appendChild(d);

    d.querySelectorAll('.opt').forEach(b=>b.addEventListener('click',()=>{
      d.querySelectorAll('.opt').forEach(x=>x.classList.remove('sel'));
      b.classList.add('sel');
      chosen[si] = +b.dataset.o;
      d.querySelector('.next').disabled = false;
    }));
    d.querySelector('.next').addEventListener('click',()=>{
      if(si===cfg.steps.length-1) finish(); else go(si+1);
    });
    d.querySelector('.prev')?.addEventListener('click',()=>go(si-1));
  });

  function go(n){
    i=n;
    root.querySelectorAll('.qstep').forEach(s=>s.classList.toggle('on', +s.dataset.i===n));
    bar.style.width = (n/cfg.steps.length*100)+'%';
    res.classList.remove('on');
    root.querySelector('.qstage').classList.remove('hide');
    window.scrollTo({top:root.offsetTop-80, behavior:'smooth'});
  }

  function finish(){
    const score = {};
    cfg.steps.forEach((st,si)=>{
      const o = st.opts[chosen[si]];
      if(!o) return;
      for(const k in o.score) score[k] = (score[k]||0) + o.score[k];
    });
    const keys = Object.keys(cfg.results);
    const max = Math.max(...keys.map(k=>score[k]||0));
    const win = keys.find(k=>(score[k]||0)===max);
    const r = cfg.results[win];

    const axes = cfg.axes || cfg.results;
    const tot = Math.max(1, ...Object.values(score));
    const bars = Object.keys(axes).map(k=>{
      const label = typeof axes[k]==='string' ? axes[k] : (axes[k].title||k);
      const v = score[k]||0;
      return `<div class="bar"><span class="t">${label}</span>
        <span class="track"><i data-w="${Math.round(v/tot*100)}"></i></span>
        <span class="v">${v}</span></div>`;
    }).join('');

    res.innerHTML = `
      <div class="res-head">
        <div class="eyebrow">${r.eyebrow||'Il tuo profilo'}</div>
        <h2>${r.title}</h2>
        <p>${r.tagline}</p>
      </div>
      <div class="bars">${bars}</div>
      ${r.html}
      <div class="qnav" style="justify-content:center;margin-top:26px">
        <button class="btn ghost" onclick="location.reload()">↻ Rifai il quiz</button>
      </div>`;
    root.querySelector('.qstage').classList.add('hide');
    res.classList.add('on');
    bar.style.width='100%';
    requestAnimationFrame(()=>res.querySelectorAll('.bar i').forEach(b=>b.style.width=b.dataset.w+'%'));
    window.scrollTo({top:root.offsetTop-80, behavior:'smooth'});
  }

  go(0);
}
