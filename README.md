<div align="center">

<br>

<svg width="400" height="80" xmlns="http://www.w3.org/2000/svg">
  <text x="50%" y="55" font-family="Georgia, serif" font-size="42" font-weight="400"
    fill="#a8c4a0" text-anchor="middle" letter-spacing="6">ANIMATOR</text>
</svg>

*jogo de adivinhação de animais com árvore avl, bfs e dfs*

<br>

![Python](https://img.shields.io/badge/python-3.8+-4a7060?style=flat&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/frontend-html%2Fjs-8faa90?style=flat)

<br>

</div>

---

## estrutura do projeto

```
animator/
├── algorithms/
│   ├── bfs.py              # busca em largura na árvore avl
│   └── dfs.py              # busca em profundidade na árvore avl
├── analysis/
│   └── comparison.py       # compara desempenho entre bfs e dfs
├── data/
│   └── zoo.csv             # dataset com 11 animais e atributos binários
├── extras/
│   └── learning.py         # módulo de aprendizado
├── frontend/
│   ├── index.html          # estrutura da interface
│   ├── style.css           # estilo visual
│   └── script.js           # lógica do jogo (avl + interface)
├── game/
│   └── play.py             # ponto de entrada: roda comparação e exporta json
├── tree/
│   ├── avl.py              # árvore avl com rotações e balanceamento
│   ├── build_tree.py       # lê o csv e monta a avl
│   └── node.py             # nó da árvore (pergunta ou resposta)
├── requirements.txt        # sem dependências externas
├── .gitignore
└── README.md
```

---

## pré-requisitos

- python 3.8+
- nenhuma biblioteca externa necessária (só módulos built-in: `csv`, `json`, `time`, `collections`)

---

## como rodar

### 1. clonar o repositório

```bash
git clone https://github.com/seu-usuario/animator.git
cd animator
```

### 2. backend (python)

```bash
python -m game.play
```

isso vai:
1. construir a árvore avl a partir do `zoo.csv`
2. rodar a comparação bfs vs dfs e imprimir as métricas no terminal
3. exportar `frontend/animais.json` com os animais

### 3. frontend (navegador)

abra o arquivo `frontend/index.html` diretamente no navegador — não precisa de servidor.

**windows:**
```bash
start frontend/index.html
```

**mac:**
```bash
open frontend/index.html
```

**linux:**
```bash
xdg-open frontend/index.html
```

ou simplesmente arraste o arquivo `index.html` para o navegador.

> os arquivos `index.html`, `style.css` e `script.js` precisam estar na mesma pasta para o jogo funcionar corretamente.

---

## como o jogo funciona

1. o jogador pensa em um dos 11 animais
2. o jogo faz perguntas de sim/não sobre atributos do animal
3. a cada resposta, candidatos são eliminados da lista
4. quando restar apenas 1 candidato, o jogo acerta

os animais disponíveis são: cavalo, gato, cachorro, tubarão, rato, baleia, tartaruga, elefante, foca, girafa e urso.

---

## estruturas e algoritmos

### árvore avl (`tree/avl.py`)

- cada animal é inserido como nó com chave gerada a partir dos atributos binários
- rotações simples e duplas garantem o balanceamento após cada inserção
- filhos `yes` e `no` representam os ramos sim/não da árvore de decisão

### bfs (`algorithms/bfs.py`)

percorre a árvore em largura usando uma fila (`deque`). visita nós nível por nível.

### dfs (`algorithms/dfs.py`)

percorre a árvore em profundidade usando uma pilha. explora cada ramo até o fim antes de retroceder.

### comparação (`analysis/comparison.py`)

executa bfs e dfs sobre a mesma árvore e compara:
- número de nós visitados
- tempo de execução em milissegundos

### frontend (`frontend/script.js`)

implementação independente em javascript com:
- avl própria para indexar os animais por atributos
- algoritmo de melhor atributo (ganho de informação) para escolher a próxima pergunta
- interface reativa que elimina candidatos a cada resposta

---

## dataset

arquivo `data/zoo.csv` com 11 animais e 13 atributos binários:

| atributo | descrição |
|---|---|
| `hair` | tem pelo |
| `feathers` | tem penas |
| `eggs` | bota ovos |
| `milk` | produz leite |
| `aquatic` | é aquático |
| `predator` | é predador |
| `toothed` | tem dentes |
| `breathes` | respira ar |
| `fins` | tem nadadeiras |
| `tem_pernas` | tem pernas |
| `tail` | tem cauda |
| `domestic` | é doméstico |
| `catsize` | é maior do que um gato |

---

## divisão de tarefas

| pessoa | arquivos |
|---|---|
| pollyana | `game/play.py`, `frontend/index.html`, `README.md` |
| lucas | `tree/node.py`, `tree/avl.py`, `tree/build_tree.py`, `analysis/comparison.py`, `frontend/style.css` |
| david | `algorithms/bfs.py`, `algorithms/dfs.py`, `extras/learning.py`, `frontend/script.js` |

---

## tecnologias

- **python 3** — backend, árvore avl, bfs, dfs
- **html / css / javascript** — frontend do jogo
- **cinzel decorative + crimson pro** — tipografia (google fonts)
- **svg** — background ilustrado da floresta
