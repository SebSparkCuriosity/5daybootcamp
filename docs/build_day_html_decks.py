#!/usr/bin/env python3
"""Build the five Digital Jersey-branded HTML facilitator decks.

Each deck is the literal run-of-show for one bootcamp day, one slide per
timed block on the real agenda (docs/DigitalJerseyFounderBootcampAgenda.pdf):
morning huddle, every Solo/Together/Out/1:1 block, every break, evening
close. Built to be put on the room's screen and stepped through once,
start to finish, as the day actually happens: keyboard/swipe/click
navigation, a progress bar, a live countdown on break slides, and a
network canvas animation on the gradient cover/closing slides (Digital
Jersey's own "tech and abstract" imagery pillar, drawn rather than stock
art).

Colours, fonts and voice rules come from the dj-presentation skill's brand
reference (references/BRAND.md). Teaching content (the Mom Test, the
positioning 2x2, overscoping, channels as a hypothesis, pricing
confidence) is written out in full, not just named, since the room reads
it straight off the screen.

Each output file is fully self-contained: Cairo and Open Sans are embedded
as base64 WOFF2 (read from docs/fonts/), so the deck opens correctly with
no network connection.

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

# Session modes, from the agenda's own legend (Solo / Together / Out / 1:1)
MODE_COLOR = {"Together": PURPLE, "1:1": NAVY, "Out": PINK, "Solo": "#9A9AA8", "Break": "#C7C7D2"}
MODE_CLASS = {"Together": "together", "1:1": "onetoone", "Out": "out", "Solo": "solo", "Break": "break"}

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
.slide-inner.break-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;height:100%;}

.slide.gradient{background:linear-gradient(135deg,__PINK__ 0%,__PURPLE__ 50%,__NAVY__ 100%);background-size:220% 220%;animation:drift 22s ease-in-out infinite;}
@keyframes drift{0%{background-position:0% 30%;}50%{background-position:100% 70%;}100%{background-position:0% 30%;}}
.slide.gradient .slide-inner::-webkit-scrollbar-thumb{background:rgba(255,255,255,.3);}
.slide.light{background:#fff;}
.slide.light.tint-together{background:#F7F4FC;}
.slide.light.tint-out{background:#FCF3FA;}
.slide.light.tint-onetoone{background:#F3F4F9;}
.slide.light.tint-break{background:#F7F7FA;}

.accent-bar{position:absolute;top:0;left:0;right:0;height:6px;z-index:3;}

canvas.network{position:absolute;inset:0;width:100%;height:100%;opacity:.75;z-index:1;}

.enter>*{opacity:0;animation:rise .6s cubic-bezier(.16,1,.3,1) forwards;animation-delay:calc(var(--i,0) * 70ms);}
@keyframes rise{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}

.slide-meta{display:flex;align-items:center;gap:12px;margin-bottom:.6em;flex-wrap:wrap;}
.slide-meta .time{font-family:'Cairo',sans-serif;font-weight:700;font-size:1.05rem;color:__NAVY__;font-variant-numeric:tabular-nums;letter-spacing:.01em;}
.slide-meta-center{font-family:'Cairo',sans-serif;font-weight:700;font-size:1.1rem;color:var(--accent);font-variant-numeric:tabular-nums;margin-bottom:.3em;letter-spacing:.02em;}

.pill{display:inline-flex;align-items:center;padding:4px 13px;border-radius:20px;font-family:'Cairo',sans-serif;font-weight:700;font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;}
.pill-together{background:__PURPLE__;color:#fff;}
.pill-onetoone{background:__NAVY__;color:#fff;}
.pill-out{background:__PINK__;color:#fff;}
.pill-solo{background:transparent;color:__META__;border:1.5px solid #D8D8E2;}
.pill-break{background:#ECECF2;color:__META__;}

.eyebrow{font-family:'Cairo',sans-serif;font-weight:700;font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;margin:0 0 .6em;}
.slide.light .eyebrow{color:var(--accent,__PURPLE__);}
.slide.gradient .eyebrow{color:__CYAN_LIGHT__;}

h1.title,h2.title{font-size:clamp(28px,4.2vw,52px);font-weight:300;line-height:1.12;white-space:pre-line;margin:0 0 .3em;text-wrap:balance;}
.slide.light h1.title,.slide.light h2.title{color:__NAVY__;}
.slide.gradient h1.title,.slide.gradient h2.title{color:#fff;}
.break-wrap h2.title{font-size:clamp(22px,3vw,34px);margin-bottom:.5em;}

.rule{width:64px;height:4px;background:var(--accent,__CYAN_LIGHT__);border-radius:2px;margin:.4em 0 .9em;}
.slide.gradient .rule{background:__CYAN_LIGHT__;}

.subtitle{font-size:clamp(15px,1.5vw,20px);font-weight:400;max-width:760px;line-height:1.55;margin:0 0 1.2em;}
.slide.light .subtitle{color:__META__;}
.slide.gradient .subtitle{color:rgba(255,255,255,.85);}

.cover-wordmark{font-family:'Cairo',sans-serif;font-weight:700;letter-spacing:.24em;font-size:.82rem;color:#fff;opacity:.88;margin-bottom:2.1em;}
.cover-number{position:absolute;top:5vh;right:5vw;font-family:'Cairo',sans-serif;font-weight:700;font-size:clamp(90px,15vw,230px);color:rgba(255,255,255,.15);line-height:1;z-index:1;pointer-events:none;}
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
.card h4{font-family:'Cairo',sans-serif;font-weight:700;font-size:1.02rem;color:__NAVY__;margin:0 0 .5em;}
.card p{font-size:.92rem;color:__GREY__;line-height:1.5;margin:0 0 .35em;}
.card ul{margin:0;padding-left:18px;}
.card li{font-size:.9rem;color:__GREY__;line-height:1.55;margin-bottom:.25em;}
.slide.gradient .card{background:rgba(255,255,255,.12);}
.slide.gradient .card h4{color:#fff;}
.slide.gradient .card p,.slide.gradient .card li{color:rgba(255,255,255,.85);}

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

.b-template{border-radius:10px;padding:20px 24px;margin:1em 0;border:1.5px dashed var(--accent,__PURPLE__);background:rgba(84,53,174,.04);}
.slide.gradient .b-template{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.5);}
.b-template p{font-family:'Cairo',sans-serif;font-weight:300;font-size:1.05rem;line-height:1.7;margin:0;}
.slide.light .b-template p{color:__NAVY__;}
.slide.gradient .b-template p{color:#fff;}
.b-template .fill{font-weight:700;color:var(--accent,__PURPLE__);}
.slide.gradient .b-template .fill{color:__CYAN_LIGHT__;}

.b-timeline{margin:.5em 0;}
.tl-row{display:grid;grid-template-columns:112px 22px 1fr;gap:0 16px;align-items:start;}
.tl-time{font-family:'Cairo',sans-serif;font-weight:700;font-size:.8rem;color:__NAVY__;padding-top:.15em;font-variant-numeric:tabular-nums;}
.tl-rail{position:relative;display:flex;justify-content:center;}
.tl-rail::before{content:"";position:absolute;top:0;bottom:-12px;width:2px;background:#E4E4F0;}
.tl-row:last-child .tl-rail::before{display:none;}
.tl-dot{width:12px;height:12px;border-radius:50%;background:var(--c,__PURPLE__);margin-top:.2em;position:relative;z-index:1;}
.tl-body{padding-bottom:14px;}
.tl-body .block{font-weight:700;color:__NAVY__;font-size:.9rem;line-height:1.35;}
.tl-body .pill{margin-top:5px;padding:2px 10px;font-size:.62rem;}

.closing-line{font-family:'Cairo',sans-serif;font-weight:300;font-size:1.15rem;color:__CYAN_LIGHT__;margin:1em 0;max-width:780px;line-height:1.45;}
.signature{margin-top:1.6em;padding-top:1.1em;border-top:1px solid rgba(255,255,255,.22);}
.signature .org{font-family:'Cairo',sans-serif;font-weight:700;color:#fff;font-size:1rem;}
.signature .line{font-size:.85rem;color:rgba(255,255,255,.72);margin-top:2px;}

.b-countdown{display:flex;flex-direction:column;align-items:center;gap:.3em;margin-top:.5em;}
.countdown-time{font-family:'Cairo',sans-serif;font-weight:700;font-size:clamp(56px,9vw,130px);color:var(--accent,__PURPLE__);font-variant-numeric:tabular-nums;line-height:1;}
.countdown-label{font-size:1.05rem;color:__META__;}

.legend{display:flex;gap:10px;flex-wrap:wrap;margin-top:1.2em;}
.legend-item{display:flex;align-items:center;gap:8px;background:#F5F5FA;border-radius:20px;padding:6px 14px 6px 8px;}
.legend-item .lg-body{font-size:.82rem;color:__GREY__;}
.legend-item .lg-body b{color:__NAVY__;}

.chrome{position:fixed;inset:0;pointer-events:none;z-index:40;}
.brand,.counter{position:absolute;top:22px;background:rgba(255,255,255,.9);color:__NAVY__;padding:7px 14px;border-radius:30px;box-shadow:0 3px 12px rgba(33,43,91,.15);backdrop-filter:blur(6px);font-family:'Cairo',sans-serif;font-weight:700;font-size:.72rem;letter-spacing:.1em;}
.brand{left:8vw;text-transform:uppercase;}
.brand .deck-name{font-weight:400;letter-spacing:.01em;opacity:.7;margin-left:10px;text-transform:none;}
.counter{right:8vw;letter-spacing:0;}
.arrow{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;border:none;background:rgba(255,255,255,.9);color:__NAVY__;font-size:1.4rem;line-height:1;cursor:pointer;pointer-events:auto;display:flex;align-items:center;justify-content:center;transition:transform .2s ease,background .2s ease;box-shadow:0 4px 14px rgba(33,43,91,.16);}
.arrow:hover{transform:translateY(-50%) scale(1.08);background:#fff;}
.arrow.prev{left:20px;}
.arrow.next{right:20px;}
.dots{position:absolute;bottom:22px;left:50%;transform:translateX(-50%);display:flex;gap:6px;pointer-events:auto;max-width:78vw;overflow-x:auto;padding:9px 14px;background:rgba(255,255,255,.9);border-radius:30px;box-shadow:0 3px 12px rgba(33,43,91,.15);backdrop-filter:blur(6px);}
.dot{width:7px;height:7px;border-radius:50%;background:rgba(33,43,91,.22);border:none;cursor:pointer;flex:none;transition:background .2s,transform .2s;padding:0;}
.dot.active{background:__PURPLE__;transform:scale(1.5);}
.hint{position:absolute;bottom:66px;left:50%;transform:translateX(-50%);font-family:'Open Sans',sans-serif;font-size:.78rem;color:rgba(255,255,255,.85);background:rgba(33,43,91,.55);padding:6px 14px;border-radius:20px;backdrop-filter:blur(4px);transition:opacity .6s ease;white-space:nowrap;}

@media (max-width:680px){
  .slide{padding:9vh 6vw 12vh;}
  .arrow{display:none;}
  .brand .deck-name{display:none;}
  .b-cards,.b-grid{grid-template-columns:1fr !important;}
  .tl-row{grid-template-columns:80px 16px 1fr;}
  .cover-stats{gap:10px;}
  .stat-plate{min-width:100px;padding:12px 14px;}
  .countdown-time{font-size:clamp(44px,16vw,80px);}
}
"""


def render_js():
    return """
const ACCENT_ROTATION = __ACCENT_ROTATION__;
const MODE_COLOR = __MODE_COLOR__;
const MODE_CLASS = __MODE_CLASS__;
const DATA = __SLIDES_JSON__;
const SIG = __SIGNATURE_JSON__;
const DAY_ACCENT = '__ACCENT__';

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
    case 'template': {
      const w=el('div','b-template');
      w.style.setProperty('--accent',accent);
      w.innerHTML=`<p>${b.html}</p>`;
      return w;
    }
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
        card.style.setProperty('--c',c.color||ACCENT_ROTATION[i%ACCENT_ROTATION.length]);
        let html=`<h4>${esc(c.title)}</h4>`;
        if(c.body) html+=`<p>${esc(c.body)}</p>`;
        if(c.items){html+='<ul>'+c.items.map(t=>`<li>${esc(t)}</li>`).join('')+'</ul>';}
        card.innerHTML=html;
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
    case 'legend': {
      const wrap=el('div','legend');
      (b.items||[]).forEach(it=>{
        const chip=el('div','legend-item');
        const dot=el('span','pill pill-'+MODE_CLASS[it.mode],esc(it.mode));
        const body=el('span','lg-body',esc(it.text));
        chip.appendChild(dot);chip.appendChild(body);
        wrap.appendChild(chip);
      });
      return wrap;
    }
    case 'countdown': {
      const wrap=el('div','b-countdown');
      wrap.style.setProperty('--accent',accent);
      wrap.dataset.until=b.until;
      const big=el('div','countdown-time','--:--');
      const lbl=el('div','countdown-label',esc(b.label||('Back at '+b.until)));
      wrap.appendChild(big);wrap.appendChild(lbl);
      return wrap;
    }
    case 'timeline': {
      const wrap=el('div','b-timeline');
      (b.rows||[]).forEach((r,i)=>{
        const row=el('div','tl-row');
        const time=el('div','tl-time',esc(r.time));
        const rail=el('div','tl-rail');
        const dot=el('div','tl-dot');
        dot.style.setProperty('--c',r.mode?MODE_COLOR[r.mode]:ACCENT_ROTATION[i%ACCENT_ROTATION.length]);
        rail.appendChild(dot);
        const body=el('div','tl-body');
        body.innerHTML=`<div class="block">${esc(r.title)}</div>`;
        if(r.mode) body.appendChild(el('span','pill pill-'+MODE_CLASS[r.mode],esc(r.mode)));
        row.appendChild(time);row.appendChild(rail);row.appendChild(body);
        wrap.appendChild(row);
      });
      return wrap;
    }
    default: return document.createTextNode('');
  }
}

function renderSlide(s){
  const kindClass=(s.kind==='cover'||s.kind==='closing')?'gradient':'light';
  const slide=el('section',`slide ${kindClass}`);
  slide.dataset.kind=s.kind;
  if(kindClass==='gradient'){
    const canvas=document.createElement('canvas');
    canvas.className='network';
    slide.appendChild(canvas);
  } else {
    const bar=el('div','accent-bar');
    bar.style.background=DAY_ACCENT;
    slide.appendChild(bar);
  }
  if(s.mode) slide.classList.add('tint-'+MODE_CLASS[s.mode]);

  const accent='__ACCENT__';

  if(s.kind==='cover' && s.number){
    slide.appendChild(el('div','cover-number',esc(s.number)));
  }

  const inner=el('div','slide-inner enter');
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
  } else if(s.kind==='break'){
    inner.classList.add('break-wrap');
    if(s.time) inner.appendChild(el('div','slide-meta-center',esc(s.time)));
    const h2=el('h2','title');h2.textContent=s.title||'Break';inner.appendChild(h2);
    inner.appendChild(renderBlock({type:'countdown',until:s.until,label:s.label},accent));
  } else {
    if(s.time||s.mode){
      const meta=el('div','slide-meta');
      if(s.time) meta.appendChild(el('span','time',esc(s.time)));
      if(s.mode) meta.appendChild(el('span','pill pill-'+MODE_CLASS[s.mode],esc(s.mode)));
      inner.appendChild(meta);
    }
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

function parseUntil(hhmm){
  const [h,m]=hhmm.split(':').map(Number);
  const d=new Date();d.setHours(h,m,0,0);return d;
}
function tickCountdowns(){
  document.querySelectorAll('.b-countdown').forEach(w=>{
    if(!w.dataset.until) return;
    const diff=parseUntil(w.dataset.until)-new Date();
    const t=w.querySelector('.countdown-time');
    if(diff<=0){t.textContent="Let's go";return;}
    const mm=Math.floor(diff/60000),ss=Math.floor((diff%60000)/1000);
    t.textContent=`${mm}:${String(ss).padStart(2,'0')}`;
  });
}
setInterval(tickCountdowns,1000);
tickCountdowns();

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
        return json.dumps(obj).replace("</", "<\\/")

    js = (
        render_js()
        .replace("__ACCENT_ROTATION__", safe_json(ACCENT_ROTATION))
        .replace("__MODE_COLOR__", safe_json(MODE_COLOR))
        .replace("__MODE_CLASS__", safe_json(MODE_CLASS))
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
# Content. Timing, session titles and modes (Solo/Together/Out/1:1/Break)
# come verbatim from the real agenda PDF. Teaching content for the named
# "Together" sessions (the Mom Test, positioning 2x2, overscoping,
# channels as a hypothesis, pricing confidence) is written out in full.
# ---------------------------------------------------------------------------

MODE_LEGEND = [
    {"mode": "Solo", "text": "You and Claude, working through the day's artefacts at your own pace."},
    {"mode": "Together", "text": "The whole room: one teaching point, then something hands-on."},
    {"mode": "Out", "text": "Away from the room, talking to real customers or prospects."},
    {"mode": "1:1", "text": "Ten to twenty minutes with Seb, on the calls that matter most."},
]


def day1_slides():
    return [
        {
            "kind": "cover", "number": "01",
            "eyebrow": "Day 1 · Monday",
            "title": "Find your\nproblem",
            "subtitle": "By tonight: a validated problem, a named segment, and real interviews in the bank.",
            "stats": [{"value": "8-12", "label": "Interviews booked"}, {"value": "09:00-17:15", "label": "Today's hours"}],
            "meta": "Digital Jersey Academy · Founder Bootcamp",
        },
        {
            "kind": "content", "title": "Today, start to finish",
            "blocks": [
                {"type": "timeline", "rows": [
                    {"time": "09:00-09:10", "title": "Morning huddle: today's number", "mode": "Together"},
                    {"time": "09:10-10:40", "title": "Develop your idea with Claude", "mode": "Solo"},
                    {"time": "10:40-10:55", "title": "Break", "mode": "Break"},
                    {"time": "10:55-11:25", "title": "Plan today's interviews", "mode": "Solo"},
                    {"time": "11:25-12:00", "title": "Write your interview script", "mode": "Solo"},
                    {"time": "12:00-12:40", "title": "The Mom Test, then a 30-second pitch round", "mode": "Together"},
                    {"time": "12:40-13:20", "title": "Lunch", "mode": "Break"},
                    {"time": "13:20-16:20", "title": "Your booked customer interviews", "mode": "Out"},
                    {"time": "16:20-16:35", "title": "Break", "mode": "Break"},
                    {"time": "16:35-17:05", "title": "Find the patterns, make the call", "mode": "1:1"},
                    {"time": "17:05-17:15", "title": "Evening close: one number, one line", "mode": "Together"},
                ]},
                {"type": "label", "text": "How the four modes work"},
                {"type": "legend", "items": MODE_LEGEND},
            ],
        },
        {
            "kind": "content", "time": "09:00-09:10", "mode": "Together", "title": "Morning huddle: today's number",
            "blocks": [
                {"type": "para", "text": "Before anything else, say today's number out loud to the room. Not a vibe, a number: a count, a deadline, a decision you'll have made by 5pm."},
                {"type": "cards", "cols": 2, "items": [
                    {"title": "A good number", "items": ["“8 interviews booked and run.”", "“A validated problem by 5pm.”"]},
                    {"title": "Not a number", "items": ["“Make progress on the idea.”", "“See how the interviews go.”"]},
                ]},
            ],
        },
        {
            "kind": "content", "time": "09:10-10:40", "mode": "Solo", "title": "Develop your idea with Claude",
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
        {"kind": "break", "time": "10:40-10:55", "title": "Break", "until": "10:55"},
        {
            "kind": "content", "time": "10:55-11:25", "mode": "Solo", "title": "Plan today's interviews",
            "blocks": [
                {"type": "para", "text": "Ten minutes per booked name turns a diary of calls into a test of your riskiest assumption."},
                {"type": "label", "text": "For every name on today's list"},
                {"type": "bullets", "items": [
                    "Who they are, and why they're worth 25 minutes",
                    "When their slot is, and how you're reaching them",
                    "The one thing this specific call has to test",
                ]},
            ],
        },
        {
            "kind": "content", "time": "11:25-12:00", "mode": "Solo", "title": "Write your interview script",
            "blocks": [
                {"type": "para", "text": "A question in your own voice survives a nervous first call; a perfect one in someone else's does not."},
                {"type": "bullets", "items": [
                    "Eight or more questions that can't be flattered",
                    "A guide for running, recording and transcribing the call",
                    "Practised out loud before the first real one",
                ]},
            ],
        },
        {
            "kind": "content", "time": "12:00-12:40", "mode": "Together", "title": "The Mom Test",
            "blocks": [
                {"type": "label", "text": "Why past behaviour beats opinion"},
                {"type": "para", "text": "Ask about their life, not your idea. Everyone is polite, everyone wants to encourage you, and asking “would you use this?” gets you a yes from your harshest critic. Opinions about the future are worthless. Specifics about the past tell the truth."},
                {"type": "cards", "cols": 2, "items": [
                    {"title": "Bad: opinions and hypotheticals", "items": [
                        "“Do you think this is a good idea?”",
                        "“Would you pay for something like this?”",
                        "“Would you use a tool that did X?”",
                    ], "color": PINK},
                    {"title": "Good: specifics about the past", "items": [
                        "“Talk me through the last time that happened.”",
                        "“What have you already tried?”",
                        "“What don't you love about how you do this today?”",
                    ], "color": CYAN_DARK},
                ]},
                {"type": "numbered", "items": [
                    {"title": "Talk about their life, not your idea", "body": "You learn nothing from their reaction to a pitch."},
                    {"title": "Ask about specifics in the past", "body": "Not generics, not opinions about the future."},
                    {"title": "Talk less, listen more", "body": "Every minute you talk is a minute they aren't."},
                ]},
                {"type": "panel", "title": "Then: 30-second pitch round", "body": "Everyone in the room pitches their idea in 30 seconds flat. Not to sell it, to hear how it sounds out loud before a stranger does."},
            ],
        },
        {"kind": "break", "time": "12:40-13:20", "title": "Lunch", "until": "13:20"},
        {
            "kind": "content", "time": "13:20-16:20", "mode": "Out", "title": "Your booked customer interviews",
            "blocks": [
                {"type": "para", "text": "Run every booked slot against the script. Listen more than you talk, and write down their exact words, not your summary of them."},
                {"type": "bullets", "items": [
                    "One record per session, logged as it happens",
                    "Their words verbatim, especially the ones that surprise you",
                    "If a call runs short, use the time to write up the last one",
                ]},
                {"type": "quote", "text": "The interviews matter more than the day.", "attribution": "p0-schedule"},
            ],
        },
        {"kind": "break", "time": "16:20-16:35", "title": "Break", "until": "16:35"},
        {
            "kind": "content", "time": "16:35-17:05", "mode": "1:1", "title": "Find the patterns, make the call",
            "blocks": [
                {"type": "para", "text": "This is the week's biggest decision: everything after today points at whatever you lock here, so a fuzzy problem now means you cannot close on Friday."},
                {"type": "numbered", "items": [
                    {"title": "Find the pattern", "body": "The same pain, in the same words, from people who don't know each other."},
                    {"title": "Name the segment", "body": "Not “everyone”, a specific group who feel this hardest."},
                    {"title": "Make the call", "body": "Persevere, pivot, or not enough evidence yet. Say it out loud with Seb."},
                ]},
            ],
        },
        {
            "kind": "closing", "title": "Evening close",
            "steps": [
                "State the number: how many interviews, what you heard",
                "Name the call: persevere, pivot, or not enough evidence yet",
                "Write it down, so tomorrow starts from truth, not memory",
            ],
            "line": "Say it out loud before you test it on a stranger.",
        },
    ]


def day2_slides():
    return [
        {
            "kind": "cover", "number": "02",
            "eyebrow": "Day 2 · Tuesday",
            "title": "Own your\ncorner",
            "subtitle": "By tonight: your positioning, your proposition, your brand and a 12-slide pitch deck.",
            "stats": [{"value": "12", "label": "Pitch deck slides"}, {"value": "09:00-17:15", "label": "Today's hours"}],
            "meta": "Digital Jersey Academy · Founder Bootcamp",
        },
        {
            "kind": "content", "title": "Today, start to finish",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:10", "title": "Morning huddle", "mode": "Together"},
                {"time": "09:10-10:10", "title": "Map the market, scan the competition, size it", "mode": "Solo"},
                {"time": "10:10-10:25", "title": "Break", "mode": "Break"},
                {"time": "10:25-11:25", "title": "Fix your positioning", "mode": "1:1"},
                {"time": "11:25-12:00", "title": "Positioning in one sentence, then a 2x2 wall gallery walk", "mode": "Together"},
                {"time": "12:00-12:45", "title": "Lunch", "mode": "Break"},
                {"time": "12:45-13:15", "title": "Craft your proposition", "mode": "Solo"},
                {"time": "13:15-13:30", "title": "Write your messaging", "mode": "Solo"},
                {"time": "13:30-14:00", "title": "Brand foundations: values, personality, tone, name", "mode": "Solo"},
                {"time": "14:00-15:00", "title": "Visual identity: logo, colours, fonts", "mode": "Solo"},
                {"time": "15:00-15:15", "title": "Break", "mode": "Break"},
                {"time": "15:15-15:45", "title": "Brand book and pitch deck assembled", "mode": "Solo"},
                {"time": "15:45-17:00", "title": "Deck review", "mode": "1:1"},
                {"time": "17:00-17:15", "title": "Evening close", "mode": "Together"},
            ]}],
        },
        {
            "kind": "content", "time": "09:00-09:10", "mode": "Together", "title": "Morning huddle",
            "blocks": [{"type": "para", "text": "Same ritual as yesterday: say today's number out loud. Today it's likely a deliverable, not a count, “a 12-slide pitch deck by 5pm”, or “my positioning statement, defended.”"}],
        },
        {
            "kind": "content", "time": "09:10-10:10", "mode": "Solo", "title": "Map the market, scan the competition, size it",
            "blocks": [{"type": "cards", "cols": 3, "items": [
                {"title": "Market map", "body": "Draw the board first: segments, value chain, named incumbents, substitutes."},
                {"title": "Competitor scan", "body": "Six or more real rivals, scored, ending on the sentence naming the gap you own."},
                {"title": "Market sizing", "body": "TAM, SAM, SOM, worked two independent ways and checked against each other."},
            ]}],
        },
        {"kind": "break", "time": "10:10-10:25", "title": "Break", "until": "10:25"},
        {
            "kind": "content", "time": "10:25-11:25", "mode": "1:1", "title": "Fix your positioning",
            "blocks": [
                {"type": "para", "text": "Bring your market map and your draft statement. Seb's job in this hour is to find the sentence where you're hedging, and make you commit."},
                {"type": "bullets", "items": [
                    "Which corner of the market you're actually fighting for",
                    "Who you're happy to lose to",
                    "The one claim no rival can honestly make",
                ]},
            ],
        },
        {
            "kind": "content", "time": "11:25-12:00", "mode": "Together", "title": "Positioning in one sentence",
            "blocks": [
                {"type": "label", "text": "The positioning statement"},
                {"type": "template", "html": "For <span class=\"fill\">[target customer]</span> who <span class=\"fill\">[has this need]</span>, <span class=\"fill\">[product]</span> is a <span class=\"fill\">[market category]</span> that <span class=\"fill\">[key benefit]</span>. Unlike <span class=\"fill\">[main alternative]</span>, we <span class=\"fill\">[real difference]</span>."},
                {"type": "label", "text": "The 2x2 map"},
                {"type": "para", "text": "Pick two axes that matter to the buyer, not to you. Plot yourself and three or four rivals. The open corner is where you win."},
                {"type": "panel", "title": "Then: wall gallery walk", "body": "Pin your 2x2 on the wall. Walk the room and read everyone else's before we talk as a group."},
            ],
        },
        {"kind": "break", "time": "12:00-12:45", "title": "Lunch", "until": "12:45"},
        {
            "kind": "content", "time": "12:45-13:15", "mode": "Solo", "title": "Craft your proposition",
            "blocks": [
                {"type": "para", "text": "A proposition is a promise you can prove: get it right and Wednesday knows what to build, and Friday's pricing has a number to anchor to."},
                {"type": "bullets", "items": ["One sentence a stranger understands first time", "The one number your customer needs to move"]},
            ],
        },
        {
            "kind": "content", "time": "13:15-13:30", "mode": "Solo", "title": "Write your messaging",
            "blocks": [
                {"type": "quote", "text": "People buy the sentence they can repeat to someone else.", "attribution": "d2-messaging"},
                {"type": "bullets", "items": ["One line", "Three proof-backed messages", "A 30-second pitch"]},
            ],
        },
        {
            "kind": "content", "time": "13:30-14:00", "mode": "Solo", "title": "Brand foundations",
            "blocks": [
                {"type": "para", "text": "Decide once how you sound and what you stand for, and every email, page and pitch downstream sounds like the same firm."},
                {"type": "bullets", "items": ["3 to 5 values", "One archetype", "A tone rated on 4 dimensions", "A resolved name, or a shortlist"]},
            ],
        },
        {
            "kind": "content", "time": "14:00-15:00", "mode": "Solo", "title": "Visual identity",
            "blocks": [
                {"type": "para", "text": "This settles how you look in under an hour, not a fortnight, and because you chose each piece yourself, you can defend it to anyone."},
                {"type": "bullets", "items": ["Three genuinely different logo concepts, pick one and refine it twice", "One of three font pairings", "A five-colour AA-safe palette"]},
            ],
        },
        {"kind": "break", "time": "15:00-15:15", "title": "Break", "until": "15:15"},
        {
            "kind": "content", "time": "15:15-15:45", "mode": "Solo", "title": "Brand book and pitch deck assembled",
            "blocks": [{"type": "panel", "title": "Brand book and pitch deck", "body": "A brand that lives in one founder's head dies at the first freelancer. The brand book is the handover; the pitch deck is tonight's homework."}],
        },
        {
            "kind": "content", "time": "15:45-17:00", "mode": "1:1", "title": "Deck review",
            "blocks": [
                {"type": "para", "text": "Seb reads your 12 slides as a stranger would: no context, no goodwill. If a slide needs you in the room to make sense, it gets cut or rewritten."},
                {"type": "bullets", "items": ["The story holds without narration", "Every claim has a number or a quote behind it", "The ask on the last slide is unmissable"]},
            ],
        },
        {
            "kind": "closing", "title": "Evening close",
            "steps": [
                "Say your positioning statement out loud, once, without notes",
                "Send the pitch deck to every founder tonight",
                "Bring the brand board tomorrow, Wednesday builds against it",
            ],
            "line": "The 2x2 tells you who you're really up against.",
        },
    ]


def day3_slides():
    return [
        {
            "kind": "cover", "number": "03",
            "eyebrow": "Day 3 · Wednesday",
            "title": "Build it",
            "subtitle": "By tonight: a live, working slice a real prospect can click, book or pay on.",
            "stats": [{"value": "3", "label": "Build paths"}, {"value": "09:00-17:15", "label": "Today's hours"}],
            "meta": "Digital Jersey Academy · Founder Bootcamp",
        },
        {
            "kind": "content", "title": "Today, start to finish",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:10", "title": "Morning huddle", "mode": "Together"},
                {"time": "09:10-09:20", "title": "Set today's product context", "mode": "Solo"},
                {"time": "09:20-09:45", "title": "Sort your requirements: Must, Should, Could, Won't", "mode": "Solo"},
                {"time": "09:45-10:15", "title": "Why builds die from overscoping, then a live wall sort", "mode": "Together"},
                {"time": "10:15-10:30", "title": "Break", "mode": "Break"},
                {"time": "10:30-11:00", "title": "Map the story: sequence the build, define done", "mode": "Solo"},
                {"time": "11:00-11:30", "title": "Build brief, blueprint, tech stack", "mode": "1:1"},
                {"time": "11:30-12:45", "title": "Domain, email and GitHub set up, build begins", "mode": "Solo"},
                {"time": "12:45-13:30", "title": "Lunch, staggered, the build keeps going", "mode": "Break"},
                {"time": "13:30-16:15", "title": "Heads-down build", "mode": "Solo"},
                {"time": "16:15-16:30", "title": "Break", "mode": "Break"},
                {"time": "16:30-17:00", "title": "Landing site goes live", "mode": "Solo"},
                {"time": "17:00-17:15", "title": "Rank what's left, evening close", "mode": "Together"},
            ]}],
        },
        {
            "kind": "content", "time": "09:00-09:10", "mode": "Together", "title": "Morning huddle",
            "blocks": [{"type": "para", "text": "Say today's number. Wednesday's is usually blunt: “a live URL by 5pm”, or the specific thing a stranger will be able to click, book or pay on."}],
        },
        {
            "kind": "content", "time": "09:10-09:20", "mode": "Solo", "title": "Set today's product context",
            "blocks": [{"type": "para", "text": "Lock in your path (software, hardware or services), write what “live and actionable” means for it, and pin your MVP to one sentence. Five minutes of clarity now stops you building the wrong thing all afternoon."}],
        },
        {
            "kind": "content", "time": "09:20-09:45", "mode": "Solo", "title": "Sort your requirements",
            "blocks": [{"type": "para", "text": "Sort every requirement into Must, Should, Could and Won't. Cap Musts at seven, on paper, before you waste build time defending a feature you invented this morning."}],
        },
        {
            "kind": "content", "time": "09:45-10:15", "mode": "Together", "title": "Why builds die from overscoping",
            "blocks": [
                {"type": "para", "text": "Every extra Must costs a Should. By tonight you need one thing that works end to end, not five things half-built. Overscoping is the single biggest reason a five-day build never ships."},
                {"type": "bullets", "items": [
                    "A Must is something a real prospect cannot act without",
                    "“It would be nice” is a Should, every time",
                    "If two people disagree whether it's a Must, it's a Should",
                ]},
                {"type": "panel", "title": "Then: live wall sort", "body": "Post every Must on the wall. Defend each one to the room in one sentence. Anyone can challenge it. If you can't defend it out loud, it's not a Must."},
            ],
        },
        {"kind": "break", "time": "10:15-10:30", "title": "Break", "until": "10:30"},
        {
            "kind": "content", "time": "10:30-11:00", "mode": "Solo", "title": "Map the story",
            "blocks": [
                {"type": "para", "text": "A MoSCoW list says what to build, not the order or the finish line. The story map draws one line through it as the MVP slice, and writes a testable “done” for every Must."},
            ],
        },
        {
            "kind": "content", "time": "11:00-11:30", "mode": "1:1", "title": "Build brief, blueprint, tech stack",
            "blocks": [
                {"type": "label", "text": "Claude drafts, you correct"},
                {"type": "para", "text": "This moves fast because it's a draft-then-explain session: Claude drafts, then walks it through in plain English and asks you to poke holes with your own domain knowledge. Your corrections reshape the draft, live, with Seb in the room."},
                {"type": "numbered", "items": [
                    {"title": "Build brief", "body": "A single brief Claude Code can build from without guessing."},
                    {"title": "Blueprint", "body": "Diagrams: what it stores, how it fits together, what it's made of."},
                    {"title": "Tech stack", "body": "One chosen stack, a monthly cost, the accounts to open."},
                ]},
                {"type": "quote", "text": "Done when you could retell the document to a friend.", "attribution": "Draft, then explain back"},
            ],
        },
        {
            "kind": "content", "time": "11:30-12:45", "mode": "Solo", "title": "Domain, email and GitHub set up, build begins",
            "blocks": [
                {"type": "para", "text": "A trust officer or law-firm partner won't enquire through something.vercel.app from a personal Gmail. A real domain and a tracked repo are the cheapest credibility you'll buy this week."},
                {"type": "bullets", "items": ["A domain you own, and business email on it", "A GitHub repo, with one issue per Must", "The build itself starts the moment setup is done"]},
            ],
        },
        {"kind": "break", "time": "12:45-13:30", "title": "Lunch", "label": "Back at 13:30, the build keeps going", "until": "13:30"},
        {
            "kind": "content", "time": "13:30-16:15", "mode": "Solo", "title": "Heads-down build",
            "blocks": [
                {"type": "label", "text": "What ships, by path"},
                {"type": "cards", "cols": 3, "items": [
                    {"title": "Software", "body": "A deployed working slice on a public URL."},
                    {"title": "Hardware", "body": "A demonstrable prototype, CAD render or physical mock, plus a pre-order or waitlist page taking real payment intent."},
                    {"title": "Services", "body": "A productised service package, one sample deliverable, plus a bookable intake page."},
                ]},
                {"type": "panel", "title": "The shared spine", "body": "A live page a real prospect can act on. That's true whatever you're building. Facilitator circulates one to one, no group session this block."},
            ],
        },
        {"kind": "break", "time": "16:15-16:30", "title": "Break", "until": "16:30"},
        {
            "kind": "content", "time": "16:30-17:00", "mode": "Solo", "title": "Landing site goes live",
            "blocks": [{"type": "para", "text": "This is the page every Thursday email, post and call points at. It has to look like you, capture leads where you can see them, and read cleanly on a phone."}],
        },
        {
            "kind": "closing", "title": "Rank what's left, evening close",
            "steps": [
                "List every open item between you and a paying customer",
                "Rank them, and name the top 3 blockers",
                "Confirm the live URL, prototype or sample actually works end to end",
            ],
            "line": "Cut scope before you cut sleep.",
        },
    ]


def day4_slides():
    return [
        {
            "kind": "cover", "number": "04",
            "eyebrow": "Day 4 · Thursday",
            "title": "Prove it",
            "subtitle": "By tonight: real usability tests done, a ranked list of buyers, and a confirmed Friday meeting.",
            "stats": [{"value": "5", "label": "Usability sessions"}, {"value": "09:00-17:25", "label": "Today's hours"}],
            "meta": "Digital Jersey Academy · Founder Bootcamp",
        },
        {
            "kind": "content", "title": "Today, start to finish",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:10", "title": "Morning huddle", "mode": "Together"},
                {"time": "09:10-09:40", "title": "Plan your usability tests, book 5 sessions", "mode": "Solo"},
                {"time": "09:40-12:40", "title": "Live usability and buying-signal tests", "mode": "Out"},
                {"time": "12:40-13:20", "title": "Lunch", "mode": "Break"},
                {"time": "13:20-13:50", "title": "Find the patterns, prioritise", "mode": "Solo"},
                {"time": "13:50-14:05", "title": "Break", "mode": "Break"},
                {"time": "14:05-14:35", "title": "Go-to-market plan: your first 10 buyers, ranked", "mode": "Solo"},
                {"time": "14:35-15:05", "title": "Choose your pricing model", "mode": "1:1"},
                {"time": "15:05-15:35", "title": "ICP, sales deck, client intake", "mode": "Solo"},
                {"time": "15:35-15:55", "title": "Build the marketing funnel", "mode": "Solo"},
                {"time": "15:55-16:25", "title": "Channels are a hypothesis, not a checklist, then a funnel wall build", "mode": "Together"},
                {"time": "16:25-16:40", "title": "Break", "mode": "Break"},
                {"time": "16:40-17:00", "title": "Onboarding pack", "mode": "Solo"},
                {"time": "17:00-17:15", "title": "Book the sale: confirmed Friday meeting", "mode": "Solo"},
                {"time": "17:15-17:25", "title": "Evening close", "mode": "Together"},
            ]}],
        },
        {
            "kind": "content", "time": "09:00-09:10", "mode": "Together", "title": "Morning huddle",
            "blocks": [{"type": "para", "text": "Say today's number: sessions booked, or the buyer you'll have confirmed for Friday by tonight."}],
        },
        {
            "kind": "content", "time": "09:10-09:40", "mode": "Solo", "title": "Plan your usability tests",
            "blocks": [
                {"type": "para", "text": "You now have a thing, so the question changes from “is the pain real?” to “does my build remove it, and is that worth money?”"},
                {"type": "bullets", "items": ["Real tasks on the live URL, not a demo you drive", "Three probes reading whether they would actually pay", "Five sessions, booked for this morning"]},
            ],
        },
        {
            "kind": "content", "time": "09:40-12:40", "mode": "Out", "title": "Live usability and buying-signal tests",
            "blocks": [
                {"type": "para", "text": "Watching five people fumble your build teaches you more than fifty surveys. Watch, don't narrate, and don't rescue them when they get stuck."},
                {"type": "bullets", "items": ["Hand them a task, then stay quiet", "Write down where they hesitate, not just where they fail", "Ask what they'd pay, only after they've used it"]},
            ],
        },
        {"kind": "break", "time": "12:40-13:20", "title": "Lunch", "until": "13:20"},
        {
            "kind": "content", "time": "13:20-13:50", "mode": "Solo", "title": "Find the patterns, prioritise",
            "blocks": [
                {"type": "quote", "text": "By Friday you can build three things not thirty and phone a handful of people, so numbers decide, not the loudest voice.", "attribution": "d4-prioritise"},
                {"type": "bullets", "items": ["Score every requested change with RICE and MoSCoW", "Rank every tester by likelihood to buy"]},
            ],
        },
        {"kind": "break", "time": "13:50-14:05", "title": "Break", "until": "14:05"},
        {
            "kind": "content", "time": "14:05-14:35", "mode": "Solo", "title": "Go-to-market plan",
            "blocks": [{"type": "quote", "text": "The warmest prospect closes far faster than a cold one, so you start there, not at the top of an alphabet.", "attribution": "d4-gtm-plan"}],
        },
        {
            "kind": "content", "time": "14:35-15:05", "mode": "1:1", "title": "Choose your pricing model",
            "blocks": [
                {"type": "para", "text": "How you charge decides who buys and how fast they say yes. This afternoon's sales deck carries a price slide, so the model and the floor get fixed now, with Seb, not guessed at alone."},
                {"type": "bullets", "items": ["Name what you charge against: the value metric", "One reason logged for every rejected model", "The exact number is tomorrow morning's first job"]},
            ],
        },
        {
            "kind": "content", "time": "15:05-15:35", "mode": "Solo", "title": "ICP, sales deck, client intake",
            "blocks": [{"type": "cards", "cols": 2, "items": [
                {"title": "ICP and sales deck", "body": "A prospect who hears their own words read back, then sees two others got the result they want, is a prospect who signs."},
                {"title": "Client intake", "body": "Most first sales die in the gap between the nod and the kickoff. Map it now: four stages, one owner, one SLA each."},
            ]}],
        },
        {
            "kind": "content", "time": "15:35-15:55", "mode": "Solo", "title": "Build the marketing funnel",
            "blocks": [{"type": "para", "text": "The path a stranger walks from first hearing about you to paying, in four stages, each with a channel, an asset and a number."}],
        },
        {
            "kind": "content", "time": "15:55-16:25", "mode": "Together", "title": "Channels are a hypothesis, not a checklist",
            "blocks": [
                {"type": "para", "text": "A channel is a bet, not a box to tick: a cost, a reach, and a conversion guess. Run the cheapest, fastest test first. Kill what shows no signal. Double down on what does."},
                {"type": "bullets", "items": [
                    "Every channel gets a number attached before you spend a day on it",
                    "A leaky step is a channel to fix or cut, not a reason to add another",
                    "One channel proven beats five half-tried",
                ]},
                {"type": "panel", "title": "Then: funnel wall build", "body": "Pin your four stages on the wall: channel, asset, number, at each one. Walk the room and defend your weakest step."},
            ],
        },
        {"kind": "break", "time": "16:25-16:40", "title": "Break", "until": "16:40"},
        {
            "kind": "content", "time": "16:40-17:00", "mode": "Solo", "title": "Onboarding pack",
            "blocks": [{"type": "para", "text": "A first week that feels handled is the cheapest retention you will ever buy. Six sections, a week-1 timeline, a named human to email."}],
        },
        {
            "kind": "content", "time": "17:00-17:15", "mode": "Solo", "title": "Book the sale",
            "blocks": [
                {"type": "numbered", "items": [
                    {"title": "Right person", "body": "Not just any contact, the warmest one from today's ranking."},
                    {"title": "Specific time", "body": "A slot on the table, not “sometime Friday”."},
                    {"title": "A reply that says yes", "body": "Confirmed before you leave the room tonight."},
                ]},
                {"type": "quote", "text": "Regulated buyers rarely take a same-day meeting, so you ask on Thursday for Friday with a time already on the table.", "attribution": "d4-book-sale"},
            ],
        },
        {
            "kind": "closing", "title": "Evening close",
            "steps": [
                "Roll call: read every name and their booked Friday time out loud",
                "Rehearse the price out loud tonight",
                "Bring your three-item fix list tomorrow, not a feature wishlist",
            ],
            "line": "Watch them use it, don't ask if they like it.",
        },
    ]


def day5_slides():
    return [
        {
            "kind": "cover", "number": "05",
            "eyebrow": "Day 5 · Friday",
            "title": "Sell it",
            "subtitle": "By tonight: your price, proposal and rehearsed pitch locked by lunchtime, then a closed deal, or a clear next step.",
            "stats": [{"value": "3", "label": "Price tiers"}, {"value": "09:00-17:00", "label": "Today's hours"}],
            "meta": "Digital Jersey Academy · Founder Bootcamp",
        },
        {
            "kind": "content", "title": "Today, start to finish",
            "blocks": [{"type": "timeline", "rows": [
                {"time": "09:00-09:10", "title": "Morning huddle", "mode": "Together"},
                {"time": "09:10-09:40", "title": "Set your price", "mode": "1:1"},
                {"time": "09:40-10:10", "title": "Say it without flinching, then a round-robin", "mode": "Together"},
                {"time": "10:10-10:25", "title": "Break", "mode": "Break"},
                {"time": "10:25-11:05", "title": "Triage and ship your top 3 fixes", "mode": "Solo"},
                {"time": "11:05-11:30", "title": "Write the proposal, prep the paperwork", "mode": "Solo"},
                {"time": "11:30-12:00", "title": "Final rehearsal", "mode": "1:1"},
                {"time": "12:00-12:45", "title": "Lunch", "mode": "Break"},
                {"time": "12:45-16:00", "title": "Speak to your prospect: the sales call", "mode": "Out"},
                {"time": "16:00-16:30", "title": "Close the deal: record the win, send the paperwork", "mode": "Solo"},
                {"time": "16:30-17:00", "title": "Review the week: index artefacts, build your audit pack", "mode": "Solo"},
            ]}],
        },
        {
            "kind": "content", "time": "09:00-09:10", "mode": "Together", "title": "Morning huddle",
            "blocks": [{"type": "para", "text": "Last one. Say today's number: your price, or the one outcome you want on the record by tonight, a signed deal or a dated next step."}],
        },
        {
            "kind": "content", "time": "09:10-09:40", "mode": "1:1", "title": "Set your price",
            "blocks": [
                {"type": "quote", "text": "Founders freeze on price, and a buyer decides in seconds whether it feels fair, so we anchor on value and engineer the middle package to win.", "attribution": "d5-price-number"},
                {"type": "bullets", "items": ["Three named packages: good, better, best", "One recommended", "Every price tied to a value assumption you can defend out loud, to Seb, first"]},
            ],
        },
        {
            "kind": "content", "time": "09:40-10:10", "mode": "Together", "title": "Say it without flinching",
            "blocks": [
                {"type": "para", "text": "State the number flat. No “but I could do a discount.” No apologising for what it costs. Say it, then stop talking and let the silence sit."},
                {"type": "numbered", "items": [
                    {"title": "Say the number, then stop talking", "body": "The next person to speak loses."},
                    {"title": "Let the silence sit", "body": "Don't fill it, don't soften it."},
                    {"title": "Answer objections without apologising", "body": "“It's too expensive” is a question, not a verdict."},
                ]},
                {"type": "panel", "title": "Then: round-robin", "body": "Everyone states their price out loud, once. The room fires back one real objection. You answer it, live."},
            ],
        },
        {"kind": "break", "time": "10:10-10:25", "title": "Break", "until": "10:25"},
        {
            "kind": "content", "time": "10:25-11:05", "mode": "Solo", "title": "Triage and ship your top 3 fixes",
            "blocks": [
                {"type": "para", "text": "Today is not for new features: it's for making one clean route work so a real person can watch it and believe it."},
                {"type": "numbered", "items": [
                    {"title": "Triage", "body": "A ruthless three-item fix list, everything else parked or roadmapped."},
                    {"title": "Ship", "body": "Build the three fixes, run the demo once end to end, commit with a timestamp."},
                ]},
            ],
        },
        {
            "kind": "content", "time": "11:05-11:30", "mode": "Solo", "title": "Write the proposal, prep the paperwork",
            "blocks": [{"type": "cards", "cols": 2, "items": [
                {"title": "Proposal", "body": "One page a named buyer can say yes to: their problem, one numeric target, a delivery window inside six weeks, one price, one next step."},
                {"title": "Paperwork", "body": "An engagement letter, terms, an invoice from the correct trading entity, and a payment method that clears today. Drafts only."},
            ]}],
        },
        {
            "kind": "content", "time": "11:30-12:00", "mode": "1:1", "title": "Final rehearsal",
            "blocks": [
                {"type": "para", "text": "One last run with Seb before the real call: the price, the objections, the close. Have a qualified lawyer review any paperwork before use, these are drafts, not final legal documents."},
                {"type": "bullets", "items": ["Say the price out loud until it stops wobbling", "8+ objections drilled", "Know your one next step if they say not yet"]},
            ],
        },
        {"kind": "break", "time": "12:00-12:45", "title": "Lunch", "until": "12:45"},
        {
            "kind": "content", "time": "12:45-16:00", "mode": "Out", "title": "Speak to your prospect",
            "blocks": [
                {"type": "para", "text": "The sales call, working the room, closing the deal. Each meeting was booked individually yesterday, so this block runs as a window, not something the whole room shares."},
                {"type": "quote", "text": "A week of work is worth nothing until someone commits, and most deals die in the last ten minutes because the founder never actually asks.", "attribution": "d5-close"},
            ],
        },
        {
            "kind": "content", "time": "16:00-16:30", "mode": "Solo", "title": "Close the deal",
            "blocks": [{"type": "bullets", "items": [
                "Record the outcome at whichever tier lands: cash, deposit, signed paid pilot, or signed LOI",
                "Send the paperwork the same hour, while the yes is still warm",
            ]}],
        },
        {
            "kind": "content", "time": "16:30-17:00", "mode": "Solo", "title": "Review the week",
            "blocks": [
                {"type": "para", "text": "Index every artefact from the week into one audit pack: the MVP, the pitch deck, the sales deck, the live page, the launch checklist. One honest link, not five scattered folders."},
                {"type": "bullets", "items": ["Every headline number stated plainly", "Target versus what actually happened", "What it takes to keep the MVP running after this week"]},
            ],
        },
        {
            "kind": "closing", "title": "See you next time",
            "steps": [
                "State your number, whatever it happened to be",
                "File the audit pack before anyone leaves",
                "Decide together what comes next",
            ],
            "line": "Say the number without flinching.",
            "signature": {"org": "Digital Jersey · Founder Bootcamp", "line": "Bring the idea. We'll bring the rest. — Seb"},
        },
    ]


DAYS = [
    ("Bootcamp Day 1: Find your problem", "Day 1", PINK, day1_slides),
    ("Bootcamp Day 2: Own your corner", "Day 2", PURPLE, day2_slides),
    ("Bootcamp Day 3: Build it", "Day 3", CYAN_DARK, day3_slides),
    ("Bootcamp Day 4: Prove it", "Day 4", CYAN_LIGHT, day4_slides),
    ("Bootcamp Day 5: Sell it", "Day 5", NAVY, day5_slides),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=os.path.join(HERE, "decks"))
    ap.add_argument("--fonts-dir", default=os.path.join(HERE, "fonts"))
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    for n, (title, label, accent, builder) in enumerate(DAYS, start=1):
        slides = builder()
        html = build_html(title, label, accent, slides, args.fonts_dir)
        path = os.path.join(args.out_dir, f"day-{n}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"wrote {path} ({len(html)/1024:.0f} KB, {len(slides)} slides)")


if __name__ == "__main__":
    main()
