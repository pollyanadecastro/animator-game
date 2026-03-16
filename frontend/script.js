// =============================================================
// script.js — Animator
// Seções: dataset, AVL, lógica do jogo, estado, interface
// =============================================================

// ── 1. DATASET — 11 animais ──────────────────────────────────

const ANIMAIS = [
  { nome:"cavalo",    hair:1, feathers:0, eggs:0, milk:1, aquatic:0, predator:0, toothed:1, breathes:1, fins:0, tem_pernas:1, tail:1, domestic:1, catsize:1 },
  { nome:"gato",      hair:1, feathers:0, eggs:0, milk:1, aquatic:0, predator:1, toothed:1, breathes:1, fins:0, tem_pernas:1, tail:1, domestic:1, catsize:0 },
  { nome:"cachorro",  hair:1, feathers:0, eggs:0, milk:1, aquatic:0, predator:1, toothed:1, breathes:1, fins:0, tem_pernas:1, tail:1, domestic:1, catsize:1 },
  { nome:"tubarão",   hair:0, feathers:0, eggs:1, milk:0, aquatic:1, predator:1, toothed:1, breathes:0, fins:1, tem_pernas:0, tail:1, domestic:0, catsize:1 },
  { nome:"rato",      hair:1, feathers:0, eggs:0, milk:1, aquatic:0, predator:0, toothed:1, breathes:1, fins:0, tem_pernas:1, tail:1, domestic:1, catsize:0 },
  { nome:"baleia",    hair:0, feathers:0, eggs:0, milk:1, aquatic:1, predator:1, toothed:1, breathes:1, fins:1, tem_pernas:0, tail:1, domestic:0, catsize:1 },
  { nome:"tartaruga", hair:0, feathers:0, eggs:1, milk:0, aquatic:1, predator:0, toothed:0, breathes:1, fins:0, tem_pernas:1, tail:1, domestic:1, catsize:0 },
  { nome:"elefante",  hair:1, feathers:0, eggs:0, milk:1, aquatic:0, predator:0, toothed:1, breathes:1, fins:0, tem_pernas:1, tail:0, domestic:0, catsize:1 },
  { nome:"foca",      hair:1, feathers:0, eggs:0, milk:1, aquatic:1, predator:1, toothed:1, breathes:1, fins:1, tem_pernas:0, tail:1, domestic:1, catsize:1 },
  { nome:"girafa",    hair:1, feathers:0, eggs:0, milk:1, aquatic:0, predator:0, toothed:1, breathes:1, fins:0, tem_pernas:1, tail:1, domestic:0, catsize:1 },
  { nome:"urso",      hair:1, feathers:0, eggs:0, milk:1, aquatic:0, predator:1, toothed:1, breathes:1, fins:0, tem_pernas:1, tail:0, domestic:0, catsize:1 },
];

const PERGUNTAS = {
  hair:       "tem pelo?",
  feathers:   "tem penas?",
  eggs:       "bota ovos?",
  milk:       "produz leite?",
  aquatic:    "é aquático?",
  predator:   "é predador?",
  toothed:    "tem dentes?",
  breathes:   "respira ar?",
  fins:       "tem nadadeiras?",
  tem_pernas: "tem pernas?",
  tail:       "tem cauda?",
  domestic:   "é doméstico?",
  catsize:    "é do tamanho de um gato ou maior?",
};

const ATRIBUTOS = Object.keys(PERGUNTAS);

// ── 2. AVL ────────────────────────────────────────────────────

class NoAVL {
  constructor(animal) {
    this.animal = animal;
    this.chave  = ATRIBUTOS.map(a => animal[a]).join('');
    this.esq    = null;
    this.dir    = null;
    this.altura = 1;
  }
}

const _h  = n => n ? n.altura : 0;
const _fb = n => n ? _h(n.esq) - _h(n.dir) : 0;
const _uh = n => { n.altura = 1 + Math.max(_h(n.esq), _h(n.dir)); };

function _rotD(z) {
  const y = z.esq, T = y.dir;
  y.dir = z; z.esq = T;
  _uh(z); _uh(y);
  return y;
}

function _rotE(z) {
  const y = z.dir, T = y.esq;
  y.esq = z; z.dir = T;
  _uh(z); _uh(y);
  return y;
}

function _bal(n) {
  _uh(n);
  const f = _fb(n);
  if (f >  1 && _fb(n.esq) >= 0) return _rotD(n);
  if (f >  1 && _fb(n.esq) <  0) { n.esq = _rotE(n.esq); return _rotD(n); }
  if (f < -1 && _fb(n.dir) <= 0) return _rotE(n);
  if (f < -1 && _fb(n.dir) >  0) { n.dir = _rotD(n.dir); return _rotE(n); }
  return n;
}

function _ins(n, animal) {
  if (!n) return new NoAVL(animal);
  const c = ATRIBUTOS.map(a => animal[a]).join('');
  if      (c < n.chave) n.esq = _ins(n.esq, animal);
  else if (c > n.chave) n.dir = _ins(n.dir, animal);
  else { n.animal = animal; return n; }
  return _bal(n);
}

let raizAVL = null;
for (const a of ANIMAIS) raizAVL = _ins(raizAVL, a);

// ── 3. LÓGICA DO JOGO ─────────────────────────────────────────

function filtrar(respostas) {
  const out = [];
  (function walk(n) {
    if (!n) return;
    walk(n.esq);
    if (Object.entries(respostas).every(([k, v]) => n.animal[k] === v)) out.push(n.animal);
    walk(n.dir);
  })(raizAVL);
  return out;
}

function melhorAtributo(candidatos, respondidos) {
  let melhor = null, score = Infinity;
  for (const a of ATRIBUTOS) {
    if (a in respondidos) continue;
    const sim = candidatos.filter(c => c[a] === 1).length;
    const nao = candidatos.length - sim;
    if (!sim || !nao) continue;
    const d = Math.abs(sim - nao);
    if (d < score) { score = d; melhor = a; }
  }
  return melhor;
}

function proximoPasso(respostas) {
  const c = filtrar(respostas);
  if (!c.length)   return { tipo: "resultado", nome: "nenhum animal encontrado 🤔" };
  if (c.length === 1) return { tipo: "resultado", nome: c[0].nome };
  const a = melhorAtributo(c, respostas);
  if (!a) return { tipo: "multiplos", nomes: c.map(x => x.nome) };
  return { tipo: "pergunta", atributo: a, texto: PERGUNTAS[a], restantes: c.length };
}

// ── 4. ESTADO ─────────────────────────────────────────────────

let respostas  = {};
let historico  = [];
let emJogo     = false;
let attrAtual  = null;
let textoAtual = null;

// ── 5. INTERFACE ──────────────────────────────────────────────

function renderLista(candidatos) {
  const el = document.getElementById('animal-list');
  el.innerHTML = '';
  const nomesCandidatos = candidatos.map(c => c.nome);
  ANIMAIS.forEach(a => {
    const ativo = nomesCandidatos.includes(a.nome);
    const div = document.createElement('div');
    div.className = 'animal-item ' + (ativo ? 'ativo' : 'eliminado');
    div.innerHTML = `<div class="animal-dot"></div><span>${a.nome}</span>`;
    el.appendChild(div);
  });
}

function setQuestion(texto, restantes) {
  const el = document.getElementById('question');
  el.style.animation = 'none';
  void el.offsetWidth;
  el.style.animation = 'slideIn 0.4s ease both';
  el.textContent = texto;
  const pct = Math.round((1 - restantes / ANIMAIS.length) * 100);
  document.getElementById('progress').style.width = pct + '%';
  document.getElementById('step-label').textContent = `${restantes} candidatos`;
  renderLista(filtrar(respostas));
}

function showResult(nome) {
  document.getElementById('game-btns').classList.add('hidden');
  document.getElementById('question').textContent = '';
  document.getElementById('result-text').textContent = nome;
  document.getElementById('result-area').classList.remove('hidden');
  document.getElementById('progress').style.width = '100%';
  document.getElementById('step-label').textContent = 'resultado!';
  const found = ANIMAIS.filter(a => a.nome === nome);
  renderLista(found.length ? found : ANIMAIS);
  buildTrail();
}

function buildTrail() {
  const c = document.getElementById('trail-items');
  c.innerHTML = '';
  historico.forEach(({ texto, resposta }) => {
    const d = document.createElement('div');
    d.className = 'trail-item';
    d.innerHTML = `<span>${texto}</span><span class="ans">${resposta}</span>`;
    c.appendChild(d);
  });
  document.getElementById('trail').classList.remove('hidden');
}

function avancar() {
  const p = proximoPasso(respostas);
  if (p.tipo === 'pergunta') {
    attrAtual  = p.atributo;
    textoAtual = p.texto;
    setQuestion(p.texto, p.restantes);
  } else if (p.tipo === 'resultado') {
    showResult(p.nome);
  } else {
    showResult(p.nomes[0]);
  }
}

function startGame() {
  respostas = {}; historico = []; emJogo = true;
  attrAtual = null; textoAtual = null;
  document.getElementById('start-btns').classList.add('hidden');
  document.getElementById('game-btns').classList.remove('hidden');
  document.getElementById('result-area').classList.add('hidden');
  document.getElementById('trail').classList.add('hidden');
  document.getElementById('trail-items').innerHTML = '';
  document.getElementById('progress').style.width = '0%';
  document.getElementById('step-label').textContent = `${ANIMAIS.length} candidatos`;
  document.getElementById('question').textContent = '';
  renderLista(ANIMAIS);
  avancar();
}

function answer(sim) {
  if (!emJogo || !attrAtual) return;
  respostas[attrAtual] = sim ? 1 : 0;
  historico.push({ texto: textoAtual, resposta: sim ? 'sim' : 'não' });
  avancar();
}

function restartGame() {
  emJogo = false;
  document.getElementById('result-area').classList.add('hidden');
  document.getElementById('game-btns').classList.add('hidden');
  document.getElementById('trail').classList.add('hidden');
  document.getElementById('start-btns').classList.remove('hidden');
  document.getElementById('progress').style.width = '0%';
  document.getElementById('step-label').textContent = '11 candidatos';
  document.getElementById('question').textContent = 'pronto para começar?';
  renderLista(ANIMAIS);
}

// init
renderLista(ANIMAIS);
