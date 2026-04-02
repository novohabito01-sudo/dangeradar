import os
import json
import urllib.parse
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>DangeRadar</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
:root{--bg:#0a0a0f;--bg2:#111118;--bg3:#18181f;--bg4:#1e1e28;--border:rgba(255,255,255,0.07);--border2:rgba(255,255,255,0.12);--text:#f0f0f5;--muted:#7b7b8f;--accent:#5b6fff;--accent2:#a78bfa;--green:#22d3a0;--amber:#f59e0b;--red:#f43f5e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:15px;min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;opacity:.03;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.glow{position:fixed;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(91,111,255,0.1) 0%,transparent 70%);top:-200px;right:-100px;pointer-events:none;z-index:0}
.app{position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:0 24px 80px}
header{padding:32px 0 40px;display:flex;align-items:center;justify-content:space-between;border-bottom:0.5px solid var(--border);margin-bottom:40px}
.logo-area{display:flex;align-items:center;gap:14px}
.logo-icon{width:42px;height:42px;background:linear-gradient(135deg,#5b6fff,#a78bfa);border-radius:12px;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:15px;color:#fff}
.logo-text{font-family:'Syne',sans-serif;font-weight:700;font-size:22px;letter-spacing:-0.5px}
.logo-text span{color:var(--accent2)}
.badge{font-size:11px;padding:4px 10px;border-radius:20px;background:rgba(91,111,255,0.15);border:0.5px solid rgba(91,111,255,0.3);color:var(--accent2);font-weight:500}
.search-label{font-family:'Syne',sans-serif;font-size:12px;font-weight:600;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px}
.search-wrap{display:flex;gap:10px;margin-bottom:32px}
.search-input{flex:1;background:var(--bg3);border:0.5px solid var(--border2);border-radius:14px;padding:14px 20px;font-size:15px;color:var(--text);font-family:'DM Sans',sans-serif;outline:none;transition:border .2s,box-shadow .2s}
.search-input::placeholder{color:var(--muted)}
.search-input:focus{border-color:rgba(91,111,255,0.5);box-shadow:0 0 0 3px rgba(91,111,255,0.1)}
.search-btn{padding:14px 28px;background:linear-gradient(135deg,#5b6fff,#a78bfa);border:none;border-radius:14px;color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:14px;cursor:pointer;transition:opacity .2s,transform .1s;white-space:nowrap}
.search-btn:hover{opacity:.9}
.search-btn:active{transform:scale(.98)}
.search-btn:disabled{opacity:.4;cursor:not-allowed}
.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:32px;padding:16px 20px;background:var(--bg3);border:0.5px solid var(--border);border-radius:14px}
.filter-group{display:flex;align-items:center;gap:8px}
.filter-label{font-size:12px;color:var(--muted);font-weight:500;white-space:nowrap}
select,.filter-input{background:var(--bg4);border:0.5px solid var(--border2);border-radius:8px;padding:7px 10px;font-size:13px;color:var(--text);font-family:'DM Sans',sans-serif;outline:none;cursor:pointer}
.filter-input{width:90px}
.filter-divider{width:0.5px;height:24px;background:var(--border);margin:0 4px}
.stats-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:32px}
.stat-card{background:var(--bg3);border:0.5px solid var(--border);border-radius:14px;padding:16px 18px;position:relative;overflow:hidden}
.stat-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:2px 2px 0 0}
.stat-card.s-accent::after{background:linear-gradient(90deg,#5b6fff,#a78bfa)}
.stat-card.s-green::after{background:var(--green)}
.stat-card.s-amber::after{background:var(--amber)}
.stat-card.s-def::after{background:var(--border2)}
.stat-label{font-size:11px;color:var(--muted);font-weight:500;letter-spacing:.8px;text-transform:uppercase;margin-bottom:8px}
.stat-value{font-family:'Syne',sans-serif;font-size:26px;font-weight:700;line-height:1}
.stat-value.green{color:var(--green)}
.stat-value.amber{color:var(--amber)}
.stat-sub{font-size:11px;color:var(--muted);margin-top:4px}
.results-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.results-title{font-family:'Syne',sans-serif;font-size:13px;font-weight:600;color:var(--muted);letter-spacing:.8px}
.results-count{font-size:13px;color:var(--muted)}
.cards{display:flex;flex-direction:column;gap:10px}
.card{background:var(--bg3);border:0.5px solid var(--border);border-radius:16px;padding:20px 22px;transition:border-color .2s,transform .15s;position:relative;overflow:hidden}
.card:hover{border-color:var(--border2);transform:translateY(-1px)}
.card.destaque{border-color:rgba(34,211,160,0.25);background:linear-gradient(135deg,rgba(34,211,160,0.04) 0%,var(--bg3) 60%)}
.card-bar{position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:3px 0 0 3px}
.card-bar.high{background:var(--green)}
.card-bar.mid{background:var(--amber)}
.card-bar.low{background:var(--red)}
.card-row1{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:10px}
.card-title{font-family:'Syne',sans-serif;font-size:14px;font-weight:600;line-height:1.4;flex:1;color:var(--text)}
.score-wrap{display:flex;flex-direction:column;align-items:flex-end;gap:3px;min-width:72px}
.score-num{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;line-height:1}
.score-num.high{color:var(--green)}
.score-num.mid{color:var(--amber)}
.score-num.low{color:var(--red)}
.score-lbl{font-size:10px;color:var(--muted);letter-spacing:.5px;text-transform:uppercase}
.score-bar-bg{width:72px;height:3px;background:var(--bg4);border-radius:2px;overflow:hidden}
.score-bar-fill{height:3px;border-radius:2px}
.card-tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.tag{font-size:11px;padding:3px 9px;border-radius:6px;font-weight:500}
.tag-catalogo{background:rgba(91,111,255,0.12);color:#8b9fff;border:0.5px solid rgba(91,111,255,0.2)}
.tag-organico{background:rgba(34,211,160,0.1);color:var(--green);border:0.5px solid rgba(34,211,160,0.2)}
.tag-tipo{background:var(--bg4);color:var(--muted);border:0.5px solid var(--border)}
.card-nums{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-bottom:12px}
.num-box{background:var(--bg4);border-radius:10px;padding:10px 8px;text-align:center}
.num-val{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:var(--text);margin-bottom:3px}
.num-lbl{font-size:10px;color:var(--muted)}
.card-footer{display:flex;align-items:center;justify-content:space-between}
.ritmo{font-size:12px;color:var(--muted)}
.ritmo span{font-weight:600}
.ritmo span.hot{color:var(--green)}
.ritmo span.warm{color:var(--amber)}
.ritmo span.cold{color:var(--muted)}
.card-link{font-size:12px;color:var(--accent2);text-decoration:none;font-weight:500;padding:5px 12px;border-radius:7px;border:0.5px solid rgba(167,139,250,0.2);background:rgba(167,139,250,0.06);transition:background .2s}
.card-link:hover{background:rgba(167,139,250,0.12)}
.destaque-crown{position:absolute;top:12px;right:14px;font-size:11px;color:var(--green);font-weight:600;background:rgba(34,211,160,0.08);border:0.5px solid rgba(34,211,160,0.2);padding:3px 8px;border-radius:6px}
.empty-state{text-align:center;padding:80px 20px;color:var(--muted)}
.empty-icon{font-size:48px;margin-bottom:16px;opacity:.4}
.empty-title{font-family:'Syne',sans-serif;font-size:18px;font-weight:600;margin-bottom:8px;color:var(--text)}
.empty-sub{font-size:14px;line-height:1.6}
.loading-state{text-align:center;padding:80px 20px}
.spinner{width:36px;height:36px;border:2.5px solid var(--border2);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite;margin:0 auto 16px}
@keyframes spin{to{transform:rotate(360deg)}}
.loading-text{font-size:14px;color:var(--muted)}
.err-box{background:rgba(244,63,94,0.08);border:0.5px solid rgba(244,63,94,0.2);border-radius:12px;padding:14px 18px;font-size:14px;color:#fb7185;margin-bottom:20px}
@media(max-width:700px){.stats-grid{grid-template-columns:repeat(2,1fr)}.card-nums{grid-template-columns:repeat(3,minmax(0,1fr))}.search-wrap{flex-direction:column}.search-btn{width:100%}}
</style>
</head>
<body>
<div class="glow"></div>
<div class="app">
  <header>
    <div class="logo-area">
      <div class="logo-icon">DR</div>
      <div>
        <div class="logo-text">Dange<span>Radar</span></div>
        <div style="font-size:12px;color:var(--muted);margin-top:1px">Inteligência de mercado — uso interno</div>
      </div>
    </div>
    <span class="badge">Etapa 1 — Beta</span>
  </header>

  <div class="search-label">Buscar nicho</div>
  <div class="search-wrap">
    <input class="search-input" id="q" type="text" placeholder="Ex: fone bluetooth, suporte celular, garrafa inox..." autocomplete="off"/>
    <button class="search-btn" id="btn" onclick="buscar()">Buscar</button>
  </div>

  <div class="filters" id="filters-box" style="display:none">
    <div class="filter-group">
      <span class="filter-label">Ordenar</span>
      <select id="sort" onchange="renderizar()">
        <option value="score">Score de oportunidade</option>
        <option value="vpd">Vendas por dia</option>
        <option value="vendas">Total de vendas</option>
        <option value="novos">Mais novos</option>
        <option value="preco_asc">Menor preço</option>
        <option value="preco_desc">Maior preço</option>
      </select>
    </div>
    <div class="filter-divider"></div>
    <div class="filter-group">
      <span class="filter-label">Tipo</span>
      <select id="ftipo" onchange="renderizar()">
        <option value="todos">Todos</option>
        <option value="organico">Orgânico</option>
        <option value="catalogo">Catálogo</option>
      </select>
    </div>
    <div class="filter-divider"></div>
    <div class="filter-group">
      <span class="filter-label">Preço R$</span>
      <input class="filter-input" type="number" id="pmin" placeholder="Min" min="0"/>
      <span class="filter-label">–</span>
      <input class="filter-input" type="number" id="pmax" placeholder="Máx" min="0"/>
      <button onclick="renderizar()" style="padding:7px 12px;background:var(--bg4);border:0.5px solid var(--border2);border-radius:8px;color:var(--text);font-size:12px;cursor:pointer">OK</button>
    </div>
  </div>

  <div class="stats-grid" id="stats" style="display:none">
    <div class="stat-card s-accent"><div class="stat-label">Resultados</div><div class="stat-value" id="st-total">0</div><div class="stat-sub">produtos encontrados</div></div>
    <div class="stat-card s-green"><div class="stat-label">Oportunidades</div><div class="stat-value green" id="st-op">0</div><div class="stat-sub">score acima de 65</div></div>
    <div class="stat-card s-amber"><div class="stat-label">Preço médio</div><div class="stat-value amber" id="st-preco">R$ 0</div><div class="stat-sub">do nicho</div></div>
    <div class="stat-card s-def"><div class="stat-label">Melhor score</div><div class="stat-value" id="st-score">0</div><div class="stat-sub">pontuação máx</div></div>
  </div>

  <div id="err-box"></div>
  <div id="rh" style="display:none" class="results-header">
    <div class="results-title">PRODUTOS ANALISADOS</div>
    <div class="results-count" id="rc"></div>
  </div>
  <div id="results">
    <div class="empty-state">
      <div class="empty-icon">🔍</div>
      <div class="empty-title">Pronto para encontrar oportunidades</div>
      <div class="empty-sub">Digite um nicho acima e clique em Buscar.<br/>O sistema analisa preço, vendas, concorrência e calcula o score.</div>
    </div>
  </div>
</div>

<script>
let dados = [];

function calcScore(p){
  let s=0;
  const v=p.sold_quantity||0, d=p.dias||0, tipo=p.listing_type_id||'', preco=p.price||0;
  if(v>1000)s+=30;else if(v>300)s+=24;else if(v>100)s+=16;else if(v>20)s+=8;
  if(d>0&&d<30)s+=28;else if(d<90)s+=20;else if(d<180)s+=12;else if(d<365)s+=6;
  if(tipo!=='gold_pro')s+=18;
  if(preco>=79&&preco<=600)s+=14;else if(preco>600)s+=7;
  if(d>0){const vpd=v/d;if(vpd>5)s+=10;else if(vpd>2)s+=6;else if(vpd>0.5)s+=3;}
  return Math.min(Math.round(s),100);
}

function diasCriacao(dt){
  if(!dt)return 0;
  try{return Math.floor((Date.now()-new Date(dt).getTime())/86400000);}catch(e){return 0;}
}

function tipoLabel(t){
  return{gold_pro:'Catálogo',gold_special:'Ouro Especial',gold:'Ouro',silver:'Prata',bronze:'Bronze',free:'Grátis'}[t]||t||'N/D';
}

function scCls(s){return s>=65?'high':s>=40?'mid':'low';}
function scColor(s){return s>=65?'#22d3a0':s>=40?'#f59e0b':'#f43f5e';}

async function mlFetch(url){
  const r = await fetch(url, {headers:{'Accept':'application/json'}});
  if(!r.ok) throw new Error('Erro '+r.status);
  return await r.json();
}

async function buscarDetalhes(items){
  const primeiros = items.slice(0,24);
  const resto = items.slice(24);
  const detalhados = await Promise.allSettled(
    primeiros.map(p =>
      mlFetch(`https://api.mercadolibre.com/items/${p.id}`).catch(()=>null)
    )
  );
  return [
    ...primeiros.map((p,i)=>{
      const det = detalhados[i].status==='fulfilled'?detalhados[i].value:null;
      if(det) Object.assign(p,{
        date_created: det.date_created||p.date_created,
        sold_quantity: det.sold_quantity??p.sold_quantity,
        listing_type_id: det.listing_type_id||p.listing_type_id,
        price: det.price||p.price
      });
      return p;
    }),
    ...resto
  ];
}

function filtrarOrdenar(){
  const tipo=document.getElementById('ftipo').value;
  const pmin=parseFloat(document.getElementById('pmin').value)||0;
  const pmax=parseFloat(document.getElementById('pmax').value)||999999;
  const sort=document.getElementById('sort').value;
  let arr=dados.filter(p=>{
    const cat=p.listing_type_id==='gold_pro';
    if(tipo==='organico'&&cat)return false;
    if(tipo==='catalogo'&&!cat)return false;
    return p.price>=pmin&&p.price<=pmax;
  });
  const m={score:(a,b)=>b._score-a._score,vpd:(a,b)=>b._vpd-a._vpd,vendas:(a,b)=>(b.sold_quantity||0)-(a.sold_quantity||0),novos:(a,b)=>a.dias-b.dias,preco_asc:(a,b)=>a.price-b.price,preco_desc:(a,b)=>b.price-a.price};
  return arr.sort(m[sort]||m.score);
}

function atualizarStats(arr){
  const box=document.getElementById('stats');
  if(!arr.length){box.style.display='none';return;}
  box.style.display='grid';
  const pm=arr.reduce((s,p)=>s+p.price,0)/arr.length;
  document.getElementById('st-total').textContent=arr.length;
  document.getElementById('st-op').textContent=arr.filter(p=>p._score>=65).length;
  document.getElementById('st-preco').textContent='R$ '+Math.round(pm).toLocaleString('pt-BR');
  document.getElementById('st-score').textContent=Math.max(...arr.map(p=>p._score));
}

function renderizar(){
  const arr=filtrarOrdenar();
  const rh=document.getElementById('rh');
  const el=document.getElementById('results');
  if(!arr.length){
    rh.style.display='none';
    el.innerHTML='<div class="empty-state"><div class="empty-icon">😕</div><div class="empty-title">Nenhum produto</div><div class="empty-sub">Tente ajustar os filtros.</div></div>';
    atualizarStats([]);return;
  }
  rh.style.display='flex';
  document.getElementById('rc').textContent=arr.length+' produtos';
  atualizarStats(arr);
  el.innerHTML=arr.map((p,i)=>{
    const sc=p._score,cls=scCls(sc),cat=p.listing_type_id==='gold_pro';
    const dest=sc>=75&&i<5;
    const vpdN=p._vpd;
    const vpdCls=vpdN>3?'hot':vpdN>0.5?'warm':'cold';
    const vpdStr=vpdN>0?vpdN.toFixed(1)+'/dia':'—';
    const margem=cat?Math.round((1-0.16-0.15)*100):Math.round((1-0.11-0.15)*100);
    return `<div class="card${dest?' destaque':''}">
      ${dest?'<span class="destaque-crown">Oportunidade</span>':''}
      <div class="card-bar ${cls}"></div>
      <div class="card-row1">
        <div class="card-title">${p.title}</div>
        <div class="score-wrap">
          <div class="score-num ${cls}">${sc}</div>
          <div class="score-lbl">score</div>
          <div class="score-bar-bg"><div class="score-bar-fill" style="width:${sc}%;background:${scColor(sc)}"></div></div>
        </div>
      </div>
      <div class="card-tags">
        <span class="tag ${cat?'tag-catalogo':'tag-organico'}">${cat?'Catálogo':'Orgânico'}</span>
        <span class="tag tag-tipo">${tipoLabel(p.listing_type_id)}</span>
      </div>
      <div class="card-nums">
        <div class="num-box"><div class="num-val">R$\u00a0${p.price.toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})}</div><div class="num-lbl">Preço</div></div>
        <div class="num-box"><div class="num-val">${(p.sold_quantity||0).toLocaleString('pt-BR')}</div><div class="num-lbl">Vendas totais</div></div>
        <div class="num-box"><div class="num-val">${p.dias>0?p.dias:'—'}</div><div class="num-lbl">Dias no ar</div></div>
        <div class="num-box"><div class="num-val ${vpdCls}">${vpdStr}</div><div class="num-lbl">Vendas/dia</div></div>
        <div class="num-box"><div class="num-val">~${margem}%</div><div class="num-lbl">Margem est.</div></div>
      </div>
      <div class="card-footer">
        <div class="ritmo">Ritmo: <span class="${vpdCls}">${vpdN>3?'Quente':vpdN>0.5?'Aquecendo':'Frio'}</span></div>
        <a class="card-link" href="https://www.mercadolivre.com.br/p/${p.id}" target="_blank">Ver no ML →</a>
      </div>
    </div>`;
  }).join('');
}

async function buscar(){
  const q=document.getElementById('q').value.trim();
  if(!q)return;
  const btn=document.getElementById('btn');
  btn.disabled=true;btn.textContent='Buscando...';
  document.getElementById('err-box').innerHTML='';
  document.getElementById('filters-box').style.display='none';
  document.getElementById('stats').style.display='none';
  document.getElementById('rh').style.display='none';
  document.getElementById('results').innerHTML='<div class="loading-state"><div class="spinner"></div><div class="loading-text">Analisando o nicho "'+q+'"...</div></div>';

  try{
   const resp=await fetch(`/api/buscar?q=${encodeURIComponent(q)}&limit=48`); 
    if(!resp.ok){const e=await resp.json();throw new Error(e.error||'Erro '+resp.status);}
    const json=await resp.json();
    
    let items=json.results||[];
    if(!items.length){
      document.getElementById('results').innerHTML='<div class="empty-state"><div class="empty-icon">😕</div><div class="empty-title">Nenhum produto encontrado</div><div class="empty-sub">Tente outro termo de busca.</div></div>';
      btn.disabled=false;btn.textContent='Buscar';return;
    }
    document.getElementById('results').innerHTML='<div class="loading-state"><div class="spinner"></div><div class="loading-text">Carregando detalhes dos produtos...</div></div>';
    items=await buscarDetalhes(items);
    dados=items.map(p=>{
      p.dias=diasCriacao(p.date_created);
      p._score=calcScore(p);
      p._vpd=p.dias>0?Math.round((p.sold_quantity||0)/p.dias*10)/10:0;
      return p;
    });
    document.getElementById('filters-box').style.display='flex';
    renderizar();
  }catch(e){
    document.getElementById('err-box').innerHTML='<div class="err-box">Erro: '+e.message+'</div>';
    document.getElementById('results').innerHTML='';
  }
  btn.disabled=false;btn.textContent='Buscar';
}

document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter')buscar();});
</script>
</body>
</html>"""

APP_ID     = "2320782848310787"
APP_SECRET = "p6guNGWcl1VJEKbQBB3amN73lkGEp029"
REDIRECT   = "https://dangeradar.onrender.com/callback"

_token_cache = {
    "token":   os.environ.get("ML_ACCESS_TOKEN"),
    "refresh": os.environ.get("ML_REFRESH_TOKEN")
}

def obter_token():
    if _token_cache["token"]:
        return _token_cache["token"]
    if _token_cache["refresh"]:
        r = requests.post("https://api.mercadolibre.com/oauth/token", data={
            "grant_type":    "refresh_token",
            "client_id":     APP_ID,
            "client_secret": APP_SECRET,
            "refresh_token": _token_cache["refresh"],
        })
        if r.status_code == 200:
            data = r.json()
            _token_cache["token"]   = data.get("access_token")
            _token_cache["refresh"] = data.get("refresh_token")
            return _token_cache["token"]
    return None

@app.route("/")
def index():
    token = obter_token()
    if not token:
        login_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>DangeRadar — Login</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet"/>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0f;color:#f0f0f5;font-family:"DM Sans",sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center}
.box{text-align:center;padding:48px;background:#18181f;border:0.5px solid rgba(255,255,255,0.1);border-radius:24px;max-width:400px;width:90%}
.logo{font-family:"Syne",sans-serif;font-size:32px;font-weight:800;margin-bottom:8px}
.logo span{color:#a78bfa}
.sub{font-size:14px;color:#7b7b8f;margin-bottom:32px}
.btn{display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#5b6fff,#a78bfa);border-radius:14px;color:#fff;font-family:"Syne",sans-serif;font-weight:700;font-size:15px;text-decoration:none;transition:opacity .2s}
.btn:hover{opacity:.9}
</style>
</head>
<body>
<div class="box">
  <div class="logo">Dange<span>Radar</span></div>
  <div class="sub">Conecte sua conta do Mercado Livre para começar</div>
  <a class="btn" href="/login">Conectar com Mercado Livre</a>
</div>
</body>
</html>"""
        return Response(login_html, mimetype="text/html")
    return Response(HTML, mimetype="text/html")

@app.route("/login")
def login():
    url = f"https://auth.mercadolivre.com/authorization?response_type=code&client_id={APP_ID}&redirect_uri={urllib.parse.quote(REDIRECT)}"
    return redirect(url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return Response("Erro: code nao encontrado", status=400)
    r = requests.post("https://api.mercadolibre.com/oauth/token", data={
        "grant_type":    "authorization_code",
        "client_id":     APP_ID,
        "client_secret": APP_SECRET,
        "code":          code,
        "redirect_uri":  REDIRECT,
    })
    print(f"Callback token: {r.status_code} {r.text}")
    if r.status_code == 200:
        data = r.json()
        _token_cache["token"]   = data.get("access_token")
        _token_cache["refresh"] = data.get("refresh_token")
        return redirect("/")
    return Response(f"Erro ao obter token: {r.text}", status=500)

@app.route("/api/buscar")
def buscar():
    q = request.args.get("q", "")
    limit = request.args.get("limit", "48")
    try:
        token = obter_token()
        if not token:
            return Response(json.dumps({"error": "Nao autenticado — acesse a pagina inicial"}), status=401, mimetype="application/json")
        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://api.mercadolibre.com/sites/MLB/search?q={urllib.parse.quote(q)}&limit={limit}"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 401:
            _token_cache["token"] = None
            token = obter_token()
            if not token:
                return Response(json.dumps({"error": "Token expirado"}), status=401, mimetype="application/json")
         headers = {}
        url = f"https://api.mercadolibre.com/sites/MLB/search
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        enriched = []
        for item in results[:24]:
            try:
                det = requests.get(
                    f"https://api.mercadolibre.com/items/{item['id']}",
                    headers=headers, timeout=8
                )
                if det.status_code == 200:
                    d = det.json()
                    for k in ["date_created","sold_quantity","listing_type_id","price"]:
                        if k in d:
                            item[k] = d[k]
            except:
                pass
            enriched.append(item)
        for item in results[24:]:
            enriched.append(item)
        resp = Response(json.dumps({"results": enriched}), mimetype="application/json")
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8765))
    app.run(host="0.0.0.0", port=port)
