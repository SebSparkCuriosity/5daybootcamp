#!/usr/bin/env python3
"""Build the five Digital Jersey-branded HTML facilitator decks.

One interactive, self-contained HTML deck per bootcamp day, replacing the
Spark PowerPoint decks with something built to be presented from a browser:
keyboard/swipe navigation, a progress bar, animated slide transitions, and
a live network animation on the gradient slides (Digital Jersey's own
"tech and abstract" imagery pillar, drawn in canvas rather than stock art).

Content and timing come straight from docs/session-plan.md and the real
skill chain in plugins/spark-bootcamp/skills/coach/references/journey-map.md.
Colours, fonts and voice rules come from the dj-presentation skill's brand
reference (references/BRAND.md), not invented.

Each output file is fully self-contained: Cairo and Open Sans are embedded
as base64 WOFF2 (read from docs/fonts/), so the deck opens correctly with
no network connection, exactly like the fallback the plugin's own
house-style deck builder uses for founders without python-pptx.

Usage:
    python3 build_day_html_decks.py [--out-dir docs/decks] [--fonts-dir docs/fonts]
"""
import argparse
import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

FONT_FILES = [
    ("Cairo", 300, "cairo-300.woff2"),
    ("Cairo", 600, "cairo-600.woff2"),
    ("Cairo", 700, "cairo-700.woff2"),
    ("Open Sans", 400, "opensans-400.woff2"),
    ("Open Sans", 600, "opensans-600.woff2"),
    ("Open Sans", 700, "opensans-700.woff2"),
]

# Digital Jersey brand palette (dj-presentation/references/BRAND.md) ------
NAVY = "#212B5B"
PURPLE = "#5435AE"
PINK = "#9F37BB"
CYAN_DARK = "#4EABF2"
CYAN_LIGHT = "#00C4FF"
GREY = "#3C3C3B"
META = "#6B6B6B"
ACCENT_ROTATION = [PINK, PURPLE, CYAN_DARK, CYAN_LIGHT, NAVY]

SIGNATURE = {"org": "Digital Jersey", "line": "digital.je"}


def font_faces(fonts_dir):
    out = []
    for family, weight, fname in FONT_FILES:
        path = os.path.join(fonts_dir, fname)
        with open(path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        out.append(
            "@font-face{font-family:'%s';font-weight:%d;font-style:normal;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}"
            % (family, weight, b64)
        )
    return "\n".join(out)


CSS = """
*,*::before,*::after{box-sizing:border-box;}
html,body{height:100%;}
body{
  margin:0;height:100vh;width:100vw;overflow:hidden;background:__NAVY__;
  font-family:'Open Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased;
}
h1,h2,h3{margin:0;font-family:'Cairo',sans-serif;font-weight:300;}

.progress{position:fixed;top:0;left:0;right:0;height:3px;background:rgba(255,255,255,.14);z-index:50;}
.progress-bar{height:100%;width:0%;background:linear-gradient(90deg,__PINK__,__CYAN_LIGHT__);transition:width .5s cubic-bezier(.22,1,.36,1);}

.stage{position:fixed;inset:0;}
.slide{
  position:absolute;inset:0;display:flex;align-items:center;padding:6vh 8vw;
  opacity:0;transform:translateY(22px) scale(.985);
  transition:opacity .45s ease,transform .55s cubic-bezier(.22,1,.36,1);
  pointer-events:none;overflow:hidden;
}
.slide.active{opacity:1;transform:translateY(0) scale(1);pointer-events:auto;z-index:2;}

.slide-inner{position:relative;z-index:2;width:100%;max-width:1180px;margin:0 auto;max-height:86vh;overflow-y:auto;padding-right:6px;}
.slide-inner::-webkit-scrollbar{width:6px;}
.slide-inner::-webkit-scrollbar-thumb{background:rgba(0,0,0,.18);border-radius:3px;}

.slide.gradient{background:linear-gradient(135deg,__PINK__ 0%,__PURPLE__ 50%,__NAVY__ 100%);background-size:220% 220%;animation:drift 22s ease-in-out infinite;}
@keyframes drift{0%{background-position:0% 30%;}50%{background-position:100% 70%;}100%{background-position:0% 30%;}}
.slide.gradient .slide-inner::-webkit-scrollbar-thumb{background:rgba(255,255,255,.3);}
.slide.light{background:#fff;}

canvas.network{position:absolute;inset:0;width:100%;height:100%;opacity:.75;z-index:1;}

.enter>*{opacity:0;animation:rise .6s cubic-bezier(.16,1,.3,1) forwards;animation-delay:calc(var(--i,0) * 70ms);}
@keyframes rise{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}

.eyebrow{font-family:'Cairo',sans-serif;font-weight:700;font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;margin:0 0 .6em;}
.slide.light .eyebrow{color:var(--accent,__PURPLE__);}
.slide.gradient .eyebrow{color:__CYAN_LIGHT__;}

h1.title,h2.title{font-size:clamp(28px,4.2vw,52px);font-weight:300;line-height:1.12;white-space:pre-line;margin:0 0 .3em;}
.slide.light h1.title,.slide.light h2.title{color:__NAVY__;}
.slide.gradient h1.title,.slide.gradient h2.title{color:#fff;}

.rule{width:64px;height:4px;background:var(--accent,__CYAN_LIGHT__);border-radius:2px;margin:.4em 0 .9em;}
.slide.gradient .rule{background:__CYAN_LIGHT__;}

.subtitle{font-size:clamp(15px,1.5vw,20px);font-weight:400;max-width:760px;line-height:1.55;margin:0 0 1.2em;}
.slide.light .subtitle{color:__META__;}
.slide.gradient .subtitle{color:rgba(255,255,255,.85);}

.cover-wordmark{font-family:'Cairo',sans-serif;font-weight:700;letter-spacing:.24em;font-size:.82rem;color:#fff;opacity:.88;margin-bottom:2.1em;}
.cover-stats{display:flex;gap:14px;margin-top:2.2em;flex-wrap:wrap;}
.stat-plate{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:10px;padding:16px 20px;min-width:120px;backdrop-filter:blur(6px);}
.stat-plate .value{font-family:'Cairo',sans-serif;font-weight:700;font-size:1.7rem;color:__CYAN_LIGHT__;}
.stat-plate .label{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.78);margin-top:2px;}
.cover-meta{margin-top:1.8em;font-size:.85rem;color:rgba(255,255,255,.62);}

.b-para{font-size:1rem;line-height:1.68;margin:0 0 1.05em;max-width:900px;}
.slide.gradient .b-para{color:rgba(255,255,255,.9);}
.slide.light .b-para{color:__GREY__;}
.b-label{font-family:'Cairo',sans-serif;font-weight:700;font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent,__PURPLE__);margin:1.1em 0 .5em;}
.slide.gradient .b-label{color:__CYAN_LIGHT__;}
.b-heading{font-family:'Cairo',sans-serif;font-weight:700;font-size:1.2rem;margin:1em 0 .4em;}
.slide.light .b-heading{color:__NAVY__;}
.slide.gradient .b-heading{color:#fff;}

.b-quote{position:relative;padding:20px 26px 20px 30px;margin:.9em 0 1.2em;border-radius:10px;}
.slide.light .b-quote{background:rgba(84,53,174,.07);}
.slide.gradient .b-quote{background:rgba(255,255,255,.12);}
.b-quote::before{content:"";position:absolute;left:0;top:10px;bottom:10px;width:4px;border-radius:2px;background:var(--accent,__CYAN_LIGHT__);}
.slide.gradient .b-quote::before{background:__CYAN_LIGHT__;}
.b-quote p{font-family:'Cairo',sans-serif;font-weight:300;font-size:1.14rem;line-height:1.48;margin:0 0 .5em;}
.slide.light .b-quote p{color:__NAVY__;}
.slide.gradient .b-quote p{color:#fff;}
.b-quote .attr{font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;}
.slide.light .b-quote .attr{color:__META__;}
.slide.gradient .b-quote .attr{color:rgba(255,255,255,.68);}

.b-bullets{list-style:none;margin:0 0 1.05em;padding:0;max-width:820px;}
.b-bullets li{position:relative;padding-left:26px;margin-bottom:.55em;line-height:1.5;}
.slide.light .b-bullets li{color:__GREY__;}
.slide.gradient .b-bullets li{color:rgba(255,255,255,.9);}
.b-bullets li::before{content:"";position:absolute;left:0;top:.5em;width:9px;height:9px;border-radius:50%;background:var(--accent,__CYAN_LIGHT__);}
.slide.gradient .b-bullets li::before{background:__CYAN_LIGHT__;}

.b-cards{display:grid;gap:16px;margin:1em 0;}
.card{background:#F5F5FA;border-radius:12px;padding:20px 22px;border-top:4px solid var(--c,__PURPLE__);transition:transform .25s ease,box-shadow .25s ease;}
.card:hover{transform:translateY(-4px);box-shadow:0 10px 24px rgba(33,43,91,.14);}
.card h4{font-family:'Cairo',sans-serif;font-weight:700;font-size:1.02rem;color:__NAVY__;margin:0 0 .4em;}
.card p{font-size:.92rem;color:__GREY__;line-height:1.5;margin:0;}
.slide.gradient .card{background:rgba(255,255,255,.12);}
.slide.gradient .card h4{color:#fff;}
.slide.gradient .card p{color:rgba(255,255,255,.85);}

.b-numbered{margin:1em 0;}
.num-row{display:flex;gap:16px;margin-bottom:16px;align-items:flex-start;}
.num-chip{flex:none;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Cairo',sans-serif;font-weight:700;color:#fff;background:var(--c,__PURPLE__);font-size:.9rem;}
.num-row h4{font-family:'Cairo',sans-serif;font-weight:700;font-size:1rem;margin:0 0 .25em;}
.slide.light .num-row h4{color:__NAVY__;}
.slide.gradient .num-row h4{color:#fff;}
.num-row p{margin:0;font-size:.92rem;line-height:1.5;}
.slide.light .num-row p{color:__GREY__;}
.slide.gradient .num-row p{color:rgba(255,255,255,.88);}

.b-grid{display:grid;gap:14px;margin:1em 0;}
.grid-tile{background:rgba(84,53,174,.07);border-radius:10px;padding:16px 18px;border-left:3px solid var(--c,__PURPLE__);}
.grid-tile .n{font-family:'Cairo',sans-serif;font-weight:700;font-size:.75rem;color:var(--c,__PURPLE__);margin-bottom:.4em;}
.grid-tile p{margin:0;font-size:.92rem;color:__GREY__;line-height:1.5;}
.slide.gradient .grid-tile{background:rgba(255,255,255,.12);}
.slide.gradient .grid-tile p{color:rgba(255,255,255,.88);}

.b-panel{border-radius:12px;padding:20px 24px;margin:1em 0;}
.slide.light .b-panel{background:__NAVY__;}
.slide.gradient .b-panel{background:rgba(255,255,255,.14);}
.b-panel h4{font-family:'Cairo',sans-serif;font-weight:700;font-size:.95rem;color:__CYAN_LIGHT__;margin:0 0 .4em;}
.b-panel p{margin:0;font-size:.9rem;color:rgba(255,255,255,.9);line-height:1.55;}

.b-timeline{margin:.5em 0;}
.tl-row{display:grid;grid-template-columns:112px 22px 1fr;gap:0 16px;align-items:start;}
.tl-time{font-family:'Cairo',sans-serif;font-weight:700;font-size:.82rem;color:__NAVY__;padding-top:.15em;}
.tl-rail{position:relative;display:flex;justify-content:center;}
.tl-rail::before{content:"";position:absolute;top:0;bottom:-14px;width:2px;background:#E4E4F0;}
.tl-row:last-child .tl-rail::before{display:none;}
.tl-dot{width:12px;height:12px;border-radius:50%;background:var(--c,__PURPLE__);margin-top:.2em;position:relative;z-index:1;}
.tl-body{padding-bottom:16px;}
.tl-body .block{font-weight:700;color:__NAVY__;font-size:.94rem;}
.tl-body .skill{font-size:.82rem;color:__META__;margin-top:2px;}

.closing-line{font-family:'Cairo',sans-serif;font-weight:300;font-size:1.15rem;color:__CYAN_LIGHT__;margin:1em 0;max-width:780px;line-height:1.45;}
.signature{margin-top:1.6em;padding-top:1.1em;border-top:1px solid rgba(255,255,255,.22);}
.signature .org{font-family:'Cairo',sans-serif;font-weight:700;color:#fff;font-size:1rem;}
.signature .line{font-size:.85rem;color:rgba(255,255,255,.72);margin-top:2px;}

.chrome{position:fixed;inset:0;pointer-events:none;z-index:40;}
.brand,.counter{position:absolute;top:22px;background:rgba(255,255,255,.9);color:__NAVY__;padding:7px 14px;border-radius:30px;box-shadow:0 3px 12px rgba(33,43,91,.15);backdrop-filter:blur(6px);font-family:'Cairo',sans-serif;font-weight:700;font-size:.72rem;letter-spacing:.1em;}
.brand{left:8vw;text-transform:uppercase;}
.brand .deck-name{font-weight:400;letter-spacing:.01em;opacity:.7;margin-left:10px;text-transform:none;}
.counter{right:8vw;letter-spacing:0;}
.arrow{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;border:none;background:rgba(255,255,255,.9);color:__NAVY__;font-size:1.4rem;line-height:1;cursor:pointer;pointer-events:auto;display:flex;align-items:center;justify-content:center;transition:transform .2s ease,background .2s ease;box-shadow:0 4px 14px rgba(33,43,91,.16);}
.arrow:hover{transform:translateY(-50%) scale(1.08);background:#fff;}
.arrow.prev{left:20px;}
.arrow.next{right:20px;}
.dots{position:absolute;bottom:22px;left:50%;transform:translateX(-50%);display:flex;gap:8px;pointer-events:auto;max-width:78vw;overflow-x:auto;padding:9px 14px;background:rgba(255,255,255,.9);border-radius:30px;box-shadow:0 3px 12px rgba(33,43,91,.15);backdrop-filter:blur(6px);}
.dot{width:8px;height:8px;border-radius:50%;background:rgba(33,43,91,.22);border:none;cursor:pointer;flex:none;transition:background .2s,transform .2s;padding:0;}
.dot.active{background:__PURPLE__;transform:scale(1.35);}
.hint{position:absolute;bottom:66px;left:50%;transform:translateX(-50%);font-family:'Open Sans',sans-serif;font-size:.78rem;color:rgba(255,255,255,.85);background:rgba(33,43,91,.55);padding:6px 14px;border-radius:20px;backdrop-filter:blur(4px);transition:opacity .6s ease;white-space:nowrap;}

@media (max-width:680px){
  .slide{padding:9vh 6vw 12vh;}
  .arrow{display:none;}
  .brand .deck-name{display:none;}
  .b-cards,.b-grid{grid-template-columns:1fr !important;}
  .tl-row{grid-template-columns:88px 18px 1fr;}
  .cover-stats{gap:10px;}
  .stat-plate{min-width:100px;padding:12px 14px;}
}
"""


def render_js():
    return """
const ACCENT_ROTATION = __ACCENT_ROTATION__;
const DATA = __SLIDES_JSON__;
const SIG = __SIGNATURE_JSON__;

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function el(tag,cls,html){const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e;}

class NetworkFX{
  constructor(canvas){
    this.canvas=canvas;this.ctx=canvas.getContext('2d');this.nodes=[];this.running=false;this.raf=null;
    this.resize=this.resize.bind(this);this.tick=this.tick.bind(this);
    window.addEventListener('resize',this.resize);
  }
  resize(){
    const r=this.canvas.getBoundingClientRect();
    const dpr=window.devicePixelRatio||1;
    this.canvas.width=Math.max(1,r.width*dpr);this.canvas.height=Math.max(1,r.height*dpr);
    this.w=r.width;this.h=r.height;
    this.ctx.setTransform(dpr,0,0,dpr,0,0);
    if(!this.nodes.length) this.seed();
  }
  seed(){
    const n=this.w<700?20:42;
    this.nodes=Array.from({length:n},()=>({x:Math.random()*this.w,y:Math.random()*this.h,vx:(Math.random()-.5)*.22,vy:(Math.random()-.5)*.22}));
  }
  start(){if(this.running)return;this.running=true;this.resize();this.raf=requestAnimationFrame(this.tick);}
  stop(){this.running=false;if(this.raf)cancelAnimationFrame(this.raf);}
  tick(){
    if(!this.running)return;
    const {ctx,w,h,nodes}=this;
    ctx.clearRect(0,0,w,h);
    for(const p of nodes){
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0||p.x>w)p.vx*=-1;
      if(p.y<0||p.y>h)p.vy*=-1;
    }
    const maxD=w<700?100:150;
    for(let i=0;i<nodes.length;i++){
      for(let j=i+1;j<nodes.length;j++){
        const a=nodes[i],b=nodes[j];
        const dx=a.x-b.x,dy=a.y-b.y;const dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<maxD){
          ctx.strokeStyle=`rgba(255,255,255,${(1-dist/maxD)*.16})`;
          ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
        }
      }
    }
    ctx.fillStyle='rgba(0,196,255,.6)';
    for(const p of nodes){ctx.beginPath();ctx.arc(p.x,p.y,1.6,0,7);ctx.fill();}
    this.raf=requestAnimationFrame(this.tick);
  }
}

function renderBlock(b,accent){
  switch(b.type){
    case 'label': return el('div','b-label',esc(b.text));
    case 'heading': return el('h3','b-heading',esc(b.text));
    case 'para': return el('p','b-para',esc(b.text));
    case 'quote': {
      const w=el('div','b-quote');
      w.style.setProperty('--accent',accent);
      w.innerHTML=`<p>${esc(b.text)}</p>`+(b.attribution?`<div class="attr">${esc(b.attribution)}</div>`:'');
      return w;
    }
    case 'bullets': {
      const ul=el('ul','b-bullets');ul.style.setProperty('--accent',accent);
      (b.items||[]).forEach(t=>ul.appendChild(el('li',null,esc(t))));
      return ul;
    }
    case 'cards': {
      const wrap=el('div','b-cards');
      wrap.style.gridTemplateColumns=`repeat(${b.cols||3},1fr)`;
      (b.items||[]).forEach((c,i)=>{
        const card=el('div','card');
        card.style.setProperty('--c',ACCENT_ROTATION[i%ACCENT_ROTATION.length]);
        card.innerHTML=`<h4>${esc(c.title)}</h4><p>${esc(c.body)}</p>`;
        wrap.appendChild(card);
      });
      return wrap;
    }
    case 'numbered': {
      const wrap=el('div','b-numbered');
      (b.items||[]).forEach((it,i)=>{
        const row=el('div','num-row');
        const chip=el('div','num-chip',String(i+1).padStart(2,'0'));
        chip.style.setProperty('--c',ACCENT_ROTATION[i%ACCENT_ROTATION.length]);
        const body=el('div');
        body.innerHTML=`<h4>${esc(it.title)}</h4>`+(it.body?`<p>${esc(it.body)}</p>`:'');
        row.appendChild(chip);row.appendChild(body);
        wrap.appendChild(row);
      });
      return wrap;
    }
    case 'grid': {
      const wrap=el('div','b-grid');
      wrap.style.gridTemplateColumns=`repeat(${b.cols||2},1fr)`;
      (b.items||[]).forEach((t,i)=>{
        const tile=el('div','grid-tile');
        tile.style.setProperty('--c',ACCENT_ROTATION[i%ACCENT_ROTATION.length]);
        tile.innerHTML=`<div class="n">${String(i+1).padStart(2,'0')}</div><p>${esc(t)}</p>`;
        wrap.appendChild(tile);
      });
      return wrap;
    }
    case 'stats': {
      const wrap=el('div','cover-stats');
      (b.items||[]).forEach(s=>{
        const p=el('div','stat-plate');
        p.innerHTML=`<div class="value">${esc(s.value)}</div><div class="label">${esc(s.label)}</div>`;
        wrap.appendChild(p);
      });
      return wrap;
    }
    case 'panel': {
      const p=el('div','b-panel');
      p.innerHTML=(b.title?`<h4>${esc(b.title)}</h4>`:'')+`<p>${esc(b.body)}</p>`;
      return p;
    }
    case 'timeline': {
      const wrap=el('div','b-timeline');
      (b.rows||[]).forEach((r,i)=>{
        const row=el('div','tl-row');
        const time=el('div','tl-time',esc(r.time));
        const rail=el('div','tl-rail');
        const dot=el('div','tl-dot');
        dot.style.setProperty('--c',ACCENT_ROTATION[i%ACCENT_ROTATION.length]);
        rail.appendChild(dot);
        const body=el('div','tl-body');
        body.innerHTML=`<div class="block">${esc(r.block)}</div><div class="skill">${esc(r.skill)}</div>`;
        row.appendChild(time);row.appendChild(rail);row.appendChild(body);
        wrap.appendChild(row);
      });
      return wrap;
    }
    default: return document.createTextNode('');
  }
}

function renderSlide(s){
  const kindClass=(s.kind==='content')?'light':'gradient';
  const slide=el('section',`slide ${kindClass}`);
  slide.dataset.kind=s.kind;
  if(kindClass==='gradient'){
    const canvas=document.createElement('canvas');
    canvas.className='network';
    slide.appendChild(canvas);
  }
  const inner=el('div','slide-inner enter');
  const accent='__ACCENT__';
  inner.style.setProperty('--accent',accent);

  if(s.kind==='cover'){
    inner.appendChild(el('div','cover-wordmark','DIGITAL JERSEY'));
    if(s.eyebrow) inner.appendChild(el('div','eyebrow',esc(s.eyebrow)));
    const h1=el('h1','title');h1.textContent=s.title;inner.appendChild(h1);
    inner.appendChild(el('div','rule'));
    if(s.subtitle) inner.appendChild(el('p','subtitle',esc(s.subtitle)));
    if(s.stats) inner.appendChild(renderBlock({type:'stats',items:s.stats},accent));
    if(s.meta) inner.appendChild(el('div','cover-meta',esc(s.meta)));
  } else if(s.kind==='closing'){
    inner.appendChild(el('div','cover-wordmark','DIGITAL JERSEY'));
    const h2=el('h2','title');h2.textContent=s.title;inner.appendChild(h2);
    inner.appendChild(el('div','rule'));
    if(s.steps){
      const wrap=el('div','b-numbered');
      s.steps.forEach((t,i)=>{
        const row=el('div','num-row');
        const chip=el('div','num-chip',String(i+1).padStart(2,'0'));
        chip.style.setProperty('--c',ACCENT_ROTATION[i%ACCENT_ROTATION.length]);
        const body=el('div');
        body.innerHTML=`<p style="margin:0;color:rgba(255,255,255,.9);font-size:.95rem;line-height:1.5;">${esc(t)}</p>`;
        row.appendChild(chip);row.appendChild(body);
        wrap.appendChild(row);
      });
      inner.appendChild(wrap);
    }
    if(s.line) inner.appendChild(el('div','closing-line',esc(s.line)));
    const sig=s.signature||SIG;
    const sigEl=el('div','signature');
    sigEl.innerHTML=`<div class="org">${esc(sig.org)}</div><div class="line">${esc(sig.line)}</div>`;
    inner.appendChild(sigEl);
  } else {
    if(s.eyebrow) inner.appendChild(el('div','eyebrow',esc(s.eyebrow)));
    const h2=el('h2','title');h2.textContent=s.title;inner.appendChild(h2);
    inner.appendChild(el('div','rule'));
    (s.blocks||[]).forEach(b=>inner.appendChild(renderBlock(b,accent)));
  }

  Array.from(inner.children).forEach((child,k)=>child.style.setProperty('--i',k));
  slide.appendChild(inner);
  return slide;
}

const stage=document.getElementById('stage');
const dotsWrap=document.getElementById('dots');
const counterCur=document.getElementById('counterCur');
const counterTotal=document.getElementById('counterTotal');
const progressBar=document.getElementById('progressBar');
const prevBtn=document.getElementById('prevBtn');
const nextBtn=document.getElementById('nextBtn');

const slideEls=DATA.map(renderSlide);
slideEls.forEach(e=>stage.appendChild(e));
counterTotal.textContent=DATA.length;

const fx=new Map();
slideEls.forEach((e,i)=>{
  const canvas=e.querySelector('canvas.network');
  if(canvas) fx.set(i,new NetworkFX(canvas));
});

DATA.forEach((_,i)=>{
  const d=document.createElement('button');
  d.className='dot';d.setAttribute('aria-label','Go to slide '+(i+1));
  d.addEventListener('click',()=>goto(i));
  dotsWrap.appendChild(d);
});
const dotEls=Array.from(dotsWrap.children);

let idx=0;
function activate(i){
  slideEls.forEach((e,k)=>{
    const active=k===i;
    e.classList.toggle('active',active);
    if(active){
      const inner=e.querySelector('.slide-inner');
      inner.classList.remove('enter');void inner.offsetWidth;inner.classList.add('enter');
    }
  });
  dotEls.forEach((d,k)=>d.classList.toggle('active',k===i));
  counterCur.textContent=i+1;
  progressBar.style.width=((i+1)/DATA.length*100)+'%';
  fx.forEach((f,k)=>k===i?f.start():f.stop());
  prevBtn.style.visibility=i===0?'hidden':'visible';
  nextBtn.style.visibility=i===DATA.length-1?'hidden':'visible';
}
function goto(i){
  idx=Math.max(0,Math.min(DATA.length-1,i));
  activate(idx);
  const h=document.getElementById('hint');
  if(h){h.style.opacity='0';setTimeout(()=>h.remove(),500);}
}

document.addEventListener('keydown',e=>{
  if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();goto(idx+1);}
  else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();goto(idx-1);}
  else if(e.key==='Home'){goto(0);}
  else if(e.key==='End'){goto(DATA.length-1);}
});
prevBtn.addEventListener('click',()=>goto(idx-1));
nextBtn.addEventListener('click',()=>goto(idx+1));

let touchX=null;
stage.addEventListener('touchstart',e=>{touchX=e.touches[0].clientX;},{passive:true});
stage.addEventListener('touchend',e=>{
  if(touchX===null)return;
  const dx=e.changedTouches[0].clientX-touchX;
  if(Math.abs(dx)>40){dx<0?goto(idx+1):goto(idx-1);}
  touchX=null;
},{passive:true});

stage.addEventListener('click',e=>{
  const x=e.clientX/window.innerWidth;
  if(x>0.62)goto(idx+1);
  else if(x<0.18)goto(idx-1);
});

setTimeout(()=>{
  const h=document.getElementById('hint');
  if(h){h.style.opacity='0';setTimeout(()=>h.remove(),600);}
},5000);

activate(0);
"""


HTML_SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__DECK_TITLE__</title>
<style>
__FONT_FACES__
__CSS__
</style>
</head>
<body>
<div class="progress"><div class="progress-bar" id="progressBar"></div></div>
<div class="stage" id="stage"></div>
<div class="chrome">
  <div class="brand">Digital Jersey<span class="deck-name">__DECK_LABEL__</span></div>
  <div class="counter"><span id="counterCur">1</span>&nbsp;/&nbsp;<span id="counterTotal"></span></div>
  <button class="arrow prev" id="prevBtn" aria-label="Previous slide">&#8249;</button>
  <button class="arrow next" id="nextBtn" aria-label="Next slide">&#8250;</button>
  <div class="dots" id="dots"></div>
  <div class="hint" id="hint">Use &#8592; &#8594; or swipe to move</div>
</div>
<script>
__JS__
</script>
</body>
</html>
"""


def build_html(deck_title, deck_label, accent, slides, fonts_dir):
    css = (
        CSS.replace("__NAVY__", NAVY)
        .replace("__PURPLE__", PURPLE)
        .replace("__PINK__", PINK)
        .replace("__CYAN_DARK__", CYAN_DARK)
        .replace("__CYAN_LIGHT__", CYAN_LIGHT)
        .replace("__GREY__", GREY)
        .replace("__META__", META)
    )
    def safe_json(obj):
        # Defends against a stray "</script" inside authored copy closing the
        # <script> tag early if that copy ever mentions markup.
        return json.dumps(obj).replace("</", "<\\/")

    js = (
        render_js()
        .replace("__ACCENT_ROTATION__", safe_json(ACCENT_ROTATION))
        .replace("__SLIDES_JSON__", safe_json(slides))
        .replace("__SIGNATURE_JSON__", safe_json(SIGNATURE))
        .replace("__ACCENT__", accent)
    )
    html = (
        HTML_SHELL.replace("__DECK_TITLE__", deck_title)
        .replace("__DECK_LABEL__", deck_label)
        .replace("__FONT_FACES__", font_faces(fonts_dir))
        .replace("__CSS__", css)
        .replace("__JS__", js)
    )
    return html


# ---------------------------------------------------------------------------
# Content, one function per day. Copy is pulled from the plugin's own
# SKILL.md "why it matters" lines and docs/session-plan.md, not invented.
# ---------------------------------------------------------------------------

def day1_slides():
    return [
        {
            "kind": "cover",
            "eyebrow": "Digital Jersey Bootcamp · Day 1",
            "title": "Day 1\nIdea and discovery",
            "subtitle": "Develop the idea deep enough to test, then hold the interviews booked weeks ago.",
            "stats": [
                {"value": "8-12", "label": "Interviews booked"},
                {"value": "6", "label": "Sessions today"},
                {"value": "09:00-17:30", "label": "Runs today"},
            ],
            "meta": "Facilitator deck · Digital Jersey",
        },
        {
            "kind": "content", "eyebrow": "Section 00", "title": "Today's schedule",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:10", "block": "Open", "skill": "Facilitator framing, coach on screen"},
                {"time": "09:10-10:15", "block": "Refine the idea", "skill": "d1-refine-idea"},
                {"time": "10:15-10:30", "block": "Break", "skill": "—"},
                {"time": "10:30-11:15", "block": "Plan the interviews", "skill": "d1-interview-plan"},
                {"time": "11:15-12:00", "block": "Write the script", "skill": "d1-write-script"},
                {"time": "12:00-13:00", "block": "Lunch, confirm today's slots", "skill": "—"},
                {"time": "13:00-17:30", "block": "Interviews, up to 8", "skill": "run-interview"},
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 01", "title": "Refine the idea",
            "blocks": [
                {"type": "para", "text": "This afternoon's interviews test a bet, and the bet has to be genuinely yours. A brief you merely nodded at will not survive contact with a real customer; one you talked into existence will."},
                {"type": "label", "text": "What we're after"},
                {"type": "bullets", "items": [
                    "Where the idea came from",
                    "What you believe, and the bet underneath it",
                    "Whose problem it is, named",
                    "One sentence: [product] helps [who] do [job] so they [get outcome]",
                ]},
                {"type": "quote", "text": "Ends with an idea brief written in your own words, not Claude's.", "attribution": "d1-refine-idea"},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 02", "title": "Plan the interviews, write the script",
            "blocks": [
                {"type": "cards", "cols": 2, "items": [
                    {"title": "Plan the interviews", "body": "Ten minutes per booked name turns a diary of calls into a test of your riskiest assumption."},
                    {"title": "Write the script", "body": "A question in your own voice survives a nervous first call; a perfect one in someone else's does not."},
                ]},
                {"type": "panel", "title": "How the facilitator runs this", "body": "One question at a time, listen, reflect back, capture their phrases word for word. Never write a line they haven't spoken to."},
            ],
        },
        {
            "kind": "divider", "eyebrow": "Section 03", "title": "Interviews begin",
            "blocks": [
                {"type": "numbered", "items": [
                    {"title": "Up to 8 in the room", "body": "25-minute slots, 10 minutes between, capped by p0-schedule."},
                    {"title": "Overflow to Tuesday", "body": "The ninth yes and beyond books Tuesday morning by default."},
                    {"title": "One record per session", "body": "Each interview writes to 01-discovery/interviews/."},
                ]},
                {"type": "quote", "text": "The interviews matter more than the day.", "attribution": "p0-schedule"},
            ],
        },
        {
            "kind": "closing", "title": "Into day 2",
            "steps": [
                "Run every booked interview against the script",
                "Log each session under 01-discovery/interviews/",
                "Overflow past slot 8 books Tuesday morning",
            ],
            "line": "Tomorrow starts with synthesis, not a fresh idea.",
        },
    ]


def day2_slides():
    return [
        {
            "kind": "cover",
            "eyebrow": "Digital Jersey Bootcamp · Day 2",
            "title": "Day 2\nMarket and proposition",
            "subtitle": "Size the market, sharpen the proposition, hand out a pitch deck.",
            "stats": [
                {"value": "11", "label": "Skills today"},
                {"value": "12", "label": "Pitch deck slides"},
                {"value": "09:00-17:00", "label": "Runs today"},
            ],
            "meta": "Facilitator deck · Digital Jersey",
        },
        {
            "kind": "content", "eyebrow": "Section 00", "title": "Today's schedule",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:35", "block": "Overflow interviews", "skill": "run-interview"},
                {"time": "09:35-10:15", "block": "Synthesise", "skill": "synthesise-interviews"},
                {"time": "10:15-10:30", "block": "Break", "skill": "—"},
                {"time": "10:30-10:50", "block": "Validate the problem, close day 1", "skill": "d1-validated-problem"},
                {"time": "10:50-11:20", "block": "Market research", "skill": "d2-market-map, -sizing, -competitor-scan"},
                {"time": "11:20-12:30", "block": "Position and propose", "skill": "d2-positioning, d2-proposition"},
                {"time": "12:30-13:30", "block": "Lunch", "skill": "—"},
                {"time": "13:30-13:40", "block": "Messaging", "skill": "d2-messaging"},
                {"time": "13:40-14:15", "block": "Brand foundations", "skill": "d2-brand-foundations"},
                {"time": "14:15-15:00", "block": "Visual identity", "skill": "d2-visual-identity, brand-register"},
                {"time": "15:00-15:15", "block": "Break", "skill": "—"},
                {"time": "15:15-15:55", "block": "Brand book, pitch deck", "skill": "d2-brand-book, d2-pitch-deck"},
                {"time": "15:55-17:00", "block": "Pitch lightning round", "skill": "group share"},
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 01", "title": "Close day 1 first",
            "blocks": [
                {"type": "label", "text": "Before market work starts"},
                {"type": "numbered", "items": [
                    {"title": "Overflow interviews", "body": "Anyone who booked Tuesday morning runs first."},
                    {"title": "Synthesise", "body": "synthesise-interviews turns the raw calls into discovery-findings.md."},
                    {"title": "Call the verdict", "body": "d1-validated-problem forces persevere, pivot, or insufficient evidence."},
                ]},
                {"type": "quote", "text": "This is the week's biggest decision: everything after day 1 points at whatever you lock here.", "attribution": "d1-validated-problem"},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 02", "title": "Market research",
            "blocks": [
                {"type": "cards", "cols": 3, "items": [
                    {"title": "Market map", "body": "Draw the board first: segments, value chain, named incumbents, substitutes."},
                    {"title": "Market sizing", "body": "TAM, SAM, SOM, worked two independent ways and checked against each other."},
                    {"title": "Competitor scan", "body": "Six or more real rivals, scored, ending on the sentence naming the gap you own."},
                ]},
                {"type": "panel", "title": "TAM / SAM / SOM", "body": "Top-down flatters you, bottom-up keeps you honest. The gap between the two methods is the assumption you haven't thought through."},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 03", "title": "Position and propose",
            "blocks": [
                {"type": "heading", "text": "Positioning"},
                {"type": "para", "text": "Positioning is the one decision that makes every later decision easier: it tells day 3 what to build, day 4 what to say, and day 5 why a prospect pays you and not the incumbent."},
                {"type": "label", "text": "The output"},
                {"type": "bullets", "items": [
                    "A Geoffrey Moore positioning statement",
                    "A 2x2 map with rivals plotted",
                    "One USP under 20 words no rival can honestly claim",
                ]},
                {"type": "heading", "text": "Proposition"},
                {"type": "para", "text": "A proposition is a promise you can prove: get it right and day 3 knows what to build and Friday's pricing has a number to anchor to."},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 04", "title": "Messaging",
            "blocks": [
                {"type": "quote", "text": "People buy the sentence they can repeat to someone else.", "attribution": "d2-messaging"},
                {"type": "bullets", "items": ["One line", "Three proof-backed messages", "A 30-second pitch"]},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 05", "title": "Brand foundations and visual identity",
            "blocks": [
                {"type": "cards", "cols": 2, "items": [
                    {"title": "Brand foundations", "body": "Decide once how you sound and what you stand for, and every email, page and pitch downstream sounds like the same firm."},
                    {"title": "Visual identity", "body": "Three genuinely different logo concepts, one font pairing, a five-colour AA-safe palette, chosen by you in under an hour."},
                ]},
                {"type": "panel", "title": "Brand book and pitch deck", "body": "A brand that lives in one founder's head dies at the first freelancer. The brand book is the handover; the pitch deck is tonight's homework."},
            ],
        },
        {
            "kind": "divider", "eyebrow": "Section 06", "title": "Pitch lightning round",
            "blocks": [{"type": "grid", "cols": 2, "items": [
                "2 minutes, one slide, no notes.",
                "A stranger in the audience should follow the whole story.",
                "Feedback from the room, then move on.",
                "Every founder presents, no exceptions.",
            ]}],
        },
        {
            "kind": "closing", "title": "Into day 3",
            "steps": [
                "Send the pitch deck to every founder tonight",
                "Sleep on the proposition before Wednesday",
                "Bring the brand board, day 3 builds against it",
            ],
            "line": "A deck forces the week's work into one clear, honest account.",
        },
    ]


def day3_slides():
    return [
        {
            "kind": "cover",
            "eyebrow": "Digital Jersey Bootcamp · Day 3",
            "title": "Day 3\nProduct and build",
            "subtitle": "Ship the smallest slice a real prospect can act on.",
            "stats": [
                {"value": "3", "label": "Business paths"},
                {"value": "7", "label": "Musts, capped"},
                {"value": "13:30-16:30", "label": "Build sprint"},
            ],
            "meta": "Facilitator deck · Digital Jersey",
        },
        {
            "kind": "content", "eyebrow": "Section 00", "title": "Today's schedule",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:15", "block": "Product context", "skill": "d3-product-context"},
                {"time": "09:15-10:15", "block": "Prioritise and map", "skill": "d3-moscow, d3-story-map"},
                {"time": "10:15-10:30", "block": "Break", "skill": "—"},
                {"time": "10:30-11:30", "block": "Draft the technical trio", "skill": "d3-prd, d3-blueprint, d3-tech-stack"},
                {"time": "11:30-12:30", "block": "Explain back, repo setup", "skill": "d3-github-setup"},
                {"time": "12:30-13:30", "block": "Lunch", "skill": "—"},
                {"time": "13:30-16:30", "block": "Build sprint", "skill": "d3-mvp-build"},
                {"time": "16:30-16:50", "block": "Domain, email, landing page", "skill": "d3-domain-email, d3-landing-site"},
                {"time": "16:50-17:00", "block": "Next steps, close day 3", "skill": "d3-next-steps"},
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 01", "title": "Scope it down",
            "blocks": [{"type": "cards", "cols": 2, "items": [
                {"title": "MoSCoW", "body": "Overscoping is the biggest reason a five-day build never ships. Musts, capped at seven."},
                {"title": "Story map", "body": "A MoSCoW list says what to build, not the order or the finish line. The map draws one line through it as the MVP slice."},
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 02", "title": "The technical trio",
            "blocks": [
                {"type": "label", "text": "Claude drafts, you correct"},
                {"type": "para", "text": "PRD, blueprint and tech stack move fast because this is a draft-then-explain skill: Claude drafts, then walks it through in plain English and asks you to poke holes with your domain knowledge. Your corrections reshape the draft."},
                {"type": "numbered", "items": [
                    {"title": "PRD", "body": "A single build brief Claude Code can build from without guessing."},
                    {"title": "Blueprint", "body": "Diagrams: what it stores, how it fits together, what it is made of."},
                    {"title": "Tech stack", "body": "One chosen stack, a monthly cost, the accounts to open, the MCP servers to connect."},
                ]},
                {"type": "quote", "text": "Done when the founder could retell the document to a friend.", "attribution": "Draft, then explain back"},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 03", "title": "What ships by 16:30",
            "blocks": [
                {"type": "label", "text": "The build sprint, by path"},
                {"type": "cards", "cols": 3, "items": [
                    {"title": "Software", "body": "A deployed working slice on a public URL."},
                    {"title": "Hardware", "body": "A demonstrable prototype, CAD render or physical mock, plus a pre-order or waitlist page taking real payment intent."},
                    {"title": "Services", "body": "A productised service package, one sample deliverable, plus a bookable intake page."},
                ]},
                {"type": "panel", "title": "The shared spine", "body": "A live page a real prospect can act on. That's true whatever you're building."},
            ],
        },
        {
            "kind": "divider", "eyebrow": "Section 04", "title": "Handoff: build sprint",
            "blocks": [
                {"type": "numbered", "items": [
                    {"title": "13:30", "body": "Facilitator circulates one to one, no group session."},
                    {"title": "16:30", "body": "Domain, email, landing page go live."},
                    {"title": "16:50", "body": "Next-steps list ranks the top 3 blockers."},
                ]},
                {"type": "quote", "text": "This is the day the idea stops being a document and becomes a thing one real person can act on.", "attribution": "d3-mvp-build"},
            ],
        },
        {
            "kind": "closing", "title": "Into day 4",
            "steps": [
                "Confirm the live URL, prototype or sample actually works end to end",
                "Book real users for tomorrow's usability tests",
                "Three blockers only, everything else waits",
            ],
            "line": "A ranked list with the three real blockers named is the difference between shipping and drifting.",
        },
    ]


def day4_slides():
    return [
        {
            "kind": "cover",
            "eyebrow": "Digital Jersey Bootcamp · Day 4",
            "title": "Day 4\nTest and go to market",
            "subtitle": "Test the build for buying signals, then build the machine that sells it.",
            "stats": [
                {"value": "5", "label": "Usability sessions"},
                {"value": "10", "label": "GTM prospects ranked"},
                {"value": "16:25", "label": "Book Friday"},
            ],
            "meta": "Facilitator deck · Digital Jersey",
        },
        {
            "kind": "content", "eyebrow": "Section 00", "title": "Today's schedule",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:15", "block": "Usability test plan", "skill": "d4-usability-plan"},
                {"time": "09:15-12:30", "block": "Usability tests", "skill": "live, real users"},
                {"time": "12:30-13:30", "block": "Lunch", "skill": "—"},
                {"time": "13:30-14:00", "block": "Synthesise feedback", "skill": "d4-prioritise"},
                {"time": "14:00-14:45", "block": "Messaging and pricing", "skill": "d4-icp-messaging, d4-pricing-model"},
                {"time": "14:45-15:00", "block": "Break", "skill": "—"},
                {"time": "15:15-16:00", "block": "Sales machine", "skill": "d4-sales-deck, intake, onboarding, funnel"},
                {"time": "16:00-16:25", "block": "GTM plan", "skill": "d4-gtm-plan"},
                {"time": "16:25-16:45", "block": "Book the Friday meeting", "skill": "d4-book-sale"},
                {"time": "16:45-17:00", "block": "Roll call, close day 4", "skill": "—"},
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 01", "title": "Usability, not bug hunting",
            "blocks": [
                {"type": "para", "text": "You now have a thing, so the question changes from ‘is the pain real?’ to ‘does my build remove it, and is that worth money?’ Watching five people fumble it teaches you more than fifty surveys."},
                {"type": "label", "text": "What we're watching for"},
                {"type": "bullets", "items": [
                    "Real tasks on the live URL, not a demo you drive",
                    "Three probes reading whether they would actually pay",
                    "Five sessions, booked ahead",
                ]},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 02", "title": "Triage the feedback",
            "blocks": [
                {"type": "quote", "text": "By Friday you can build three things not thirty and phone a handful of people, so numbers decide, not the loudest voice.", "attribution": "d4-prioritise"},
                {"type": "bullets", "items": ["Score every requested change with RICE and MoSCoW", "Rank every tester by likelihood to buy"]},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 03", "title": "Messaging and pricing",
            "blocks": [{"type": "cards", "cols": 2, "items": [
                {"title": "ICP and messaging", "body": "On Friday you reach only a handful of people and say roughly the same thing to each, so fuzzy targeting costs you half of them."},
                {"title": "Pricing model", "body": "How you charge decides who buys and how fast they say yes. The model and floor get fixed now; the exact number is Friday's first job."},
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 04", "title": "The sales machine",
            "blocks": [{"type": "grid", "cols": 2, "items": [
                "Sales deck: a prospect who hears their own words read back is a prospect who signs.",
                "Intake process: most first sales die in the gap between the nod and the kickoff.",
                "Onboarding pack: a first week that feels handled is the cheapest retention you will ever buy.",
                "Marketing funnel: how many arrive, and how many carry on.",
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 05", "title": "GTM plan",
            "blocks": [{"type": "quote", "text": "The warmest prospect closes far faster than a cold one, so you start there, not at the top of an alphabet.", "attribution": "d4-gtm-plan"}],
        },
        {
            "kind": "divider", "eyebrow": "Section 06", "title": "The gate: book the Friday meeting",
            "blocks": [
                {"type": "numbered", "items": [
                    {"title": "Right person", "body": "Not just any contact, the warmest one from today's ranking."},
                    {"title": "Specific time", "body": "A slot on the table, not ‘sometime Friday’."},
                    {"title": "A reply that says yes", "body": "Confirmed before anyone leaves the room."},
                ]},
                {"type": "quote", "text": "Regulated buyers rarely take a same-day meeting, so you ask on Thursday for Friday with a time already on the table.", "attribution": "d4-book-sale"},
                {"type": "panel", "title": "Nobody leaves without it", "body": "Roll call at 16:45: read every name and their booked time out loud."},
            ],
        },
        {
            "kind": "closing", "title": "Into day 5",
            "steps": [
                "Confirm your Friday meeting time and channel",
                "Rehearse the price out loud tonight",
                "Bring your three-item fix list, not a feature wishlist",
            ],
            "line": "On day 5 you have hours and one job: get a real prospect to act on your live page.",
        },
    ]


def day5_slides():
    return [
        {
            "kind": "cover",
            "eyebrow": "Digital Jersey Bootcamp · Day 5",
            "title": "Day 5\nTweaks and first sale",
            "subtitle": "Hit the headline number, a real customer commits.",
            "stats": [
                {"value": "3", "label": "Fixes, ruthlessly"},
                {"value": "3", "label": "Price tiers"},
                {"value": "13:45-16:00", "label": "Sale meetings"},
            ],
            "meta": "Facilitator deck · Digital Jersey",
        },
        {
            "kind": "content", "eyebrow": "Section 00", "title": "Today's schedule",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:20", "block": "Triage yesterday's feedback", "skill": "d5-triage"},
                {"time": "09:20-10:30", "block": "Ship the fixes", "skill": "d5-ship-fixes"},
                {"time": "10:30-10:45", "block": "Break", "skill": "—"},
                {"time": "10:45-11:10", "block": "Set the price", "skill": "d5-price-number"},
                {"time": "11:10-11:35", "block": "Draft the proposal", "skill": "d5-proposal"},
                {"time": "11:35-12:30", "block": "Paperwork", "skill": "d5-paperwork"},
                {"time": "12:30-13:15", "block": "Lunch, early", "skill": "—"},
                {"time": "13:15-13:45", "block": "Rehearse in pairs", "skill": "d5-rehearse"},
                {"time": "13:45-16:00", "block": "Sale meetings, staggered", "skill": "live, off the plugin"},
                {"time": "16:00-16:20", "block": "Log the outcome", "skill": "d5-close"},
                {"time": "16:20-16:50", "block": "Compile the launch package", "skill": "d5-review"},
                {"time": "16:50-17:00", "block": "Demo day: state your number", "skill": "group close"},
            ]}],
        },
        {
            "kind": "content", "eyebrow": "Section 01", "title": "Triage and ship",
            "blocks": [
                {"type": "quote", "text": "On day 5 you have hours and one job: get a real prospect to act on your live page, so fixing everything means shipping nothing.", "attribution": "d5-triage"},
                {"type": "para", "text": "Friday is not for new features: it is for making one clean route work so a real person can watch it and believe it."},
                {"type": "numbered", "items": [
                    {"title": "Triage", "body": "A ruthless three-item fix list, everything else parked or roadmapped."},
                    {"title": "Ship", "body": "Build the three fixes, run the demo once end to end, commit with a timestamp."},
                ]},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 02", "title": "Set the price",
            "blocks": [
                {"type": "quote", "text": "Founders freeze on price, and a buyer decides in seconds whether it feels fair, so we anchor on value and engineer the middle package to win.", "attribution": "d5-price-number"},
                {"type": "bullets", "items": [
                    "Three named packages: good, better, best",
                    "One recommended",
                    "Every price tied to a value assumption you can defend out loud",
                ]},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 03", "title": "Proposal and paperwork",
            "blocks": [
                {"type": "cards", "cols": 2, "items": [
                    {"title": "Proposal", "body": "One page a named buyer can say yes to: their problem, one numeric target, a delivery window inside six weeks, one price, one next step."},
                    {"title": "Paperwork", "body": "An engagement letter, terms, an invoice from the correct trading entity, and a payment method that clears today. Drafts only."},
                ]},
                {"type": "panel", "title": "Have a qualified lawyer review this before use", "body": "These are drafts, not final legal documents."},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 04", "title": "Rehearse",
            "blocks": [
                {"type": "quote", "text": "The sale is won by naming the price without flinching and answering “it's too expensive” without apologising.", "attribution": "d5-rehearse"},
                {"type": "bullets", "items": ["A full sales role-play", "8+ objections drilled", "Say the price out loud until it stops wobbling"]},
            ],
        },
        {
            "kind": "divider", "eyebrow": "Section 05", "title": "Sale meetings",
            "blocks": [
                {"type": "para", "text": "Each founder's Friday meeting was booked individually on day 4. The room runs as a window, not a block everyone shares."},
                {"type": "label", "text": "13:45-16:00"},
            ],
        },
        {
            "kind": "content", "eyebrow": "Section 06", "title": "Close and review",
            "blocks": [
                {"type": "quote", "text": "A week of work is worth nothing until someone commits, and most deals die in the last ten minutes because the founder never actually asks.", "attribution": "d5-close"},
                {"type": "bullets", "items": [
                    "Record the outcome at whichever tier lands: cash, deposit, signed paid pilot, or signed LOI",
                    "Compile LAUNCH-PACKAGE.md: every headline number, target versus achieved",
                ]},
            ],
        },
        {
            "kind": "closing", "title": "Demo day",
            "steps": [
                "State your number, whatever it is",
                "One honest link: MVP, pitch deck, sales deck, live page, launch checklist",
                "Decide together what Monday looks like",
            ],
            "line": "By Friday your week is scattered across five folders; this gives one honest link.",
        },
    ]


DAYS = [
    ("Day 1: Idea and discovery · Digital Jersey Bootcamp", "Day 1", PINK, day1_slides),
    ("Day 2: Market and proposition · Digital Jersey Bootcamp", "Day 2", PURPLE, day2_slides),
    ("Day 3: Product and build · Digital Jersey Bootcamp", "Day 3", CYAN_DARK, day3_slides),
    ("Day 4: Test and go to market · Digital Jersey Bootcamp", "Day 4", CYAN_LIGHT, day4_slides),
    ("Day 5: Tweaks and first sale · Digital Jersey Bootcamp", "Day 5", NAVY, day5_slides),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=os.path.join(HERE, "decks"))
    ap.add_argument("--fonts-dir", default=os.path.join(HERE, "fonts"))
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    for n, (title, label, accent, builder) in enumerate(DAYS, start=1):
        html = build_html(title, label, accent, builder(), args.fonts_dir)
        path = os.path.join(args.out_dir, f"day-{n}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"wrote {path} ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
