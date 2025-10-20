# 🤖 Painel IA dos Mercados

Aplicação Flask que usa **inteligência artificial simples e indicadores técnicos** (RSI, EMA, Momentum, Volatilidade) para prever a tendência de três mercados:

- 🌍 **Global:** S&P 500, Dow Jones, Nasdaq  
- 🇪🇺 **Europa:** EuroStoxx50, CAC 40  
- ₿ **Cripto:** Bitcoin e Ethereum  

Inclui gráficos interativos, som IA, animação de partículas e glossário técnico.

---

## 🚀 Funcionalidades

✅ Painel interativo com IA preditiva  
✅ Gráficos automáticos com histórico de probabilidade  
✅ Atualização automática a cada minuto  
✅ Glossário técnico com *tooltips* explicativos  
✅ Design futurista e responsivo  
✅ Compatível com **Vercel** e execução local

---

## 📦 Estrutura do Projeto

```
painel-ia-dos-mercados/
│
├── app.py
├── requirements.txt
├── vercel.json
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── bip.mp3
│
└── README.md
```

---

## 🧰 Requisitos

- Python **3.9 ou superior**
- Pip atualizado (`pip install --upgrade pip`)

---

## 💻 Como Correr Localmente (Guia para Iniciantes)

### 🧩 1️⃣ Instalar o Python

1. Vai a 👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Faz **download da versão 3.10 ou superior**
3. Marca a opção ✅ *“Add Python to PATH”*
4. Confirma a instalação:
   ```bash
   python --version
   ```

---

### 📦 2️⃣ Fazer Download da App

#### 🔹 Opção A — Via GitHub
1. Abre o repositório do projeto  
2. Clica em **Code → Download ZIP**
3. Extrai o ficheiro ZIP

#### 🔹 Opção B — Manualmente
Cria uma pasta e copia os ficheiros:
```
app.py
requirements.txt
vercel.json
templates/
static/
```

---

### ⚙️ 3️⃣ Instalar as dependências

Abre o terminal na pasta onde está o `app.py` e executa:

```bash
pip install -r requirements.txt
```

---

### 🚀 4️⃣ Correr a aplicação

```bash
python app.py
```

Depois abre o navegador em:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### 🎵 5️⃣ Verifica se tudo está a funcionar

- Deves ouvir um **bip IA**  
- Ver **3 painéis** (Global, Europa, Cripto)  
- E um **Glossário Técnico IA** no rodapé  

---

### 🧠 6️⃣ (Opcional) Atualizar Dependências

```bash
pip install --upgrade flask yfinance pandas numpy
```

---

### 🧩 7️⃣ (Opcional) Parar o servidor

Pressiona `CTRL + C` no terminal.

---

## ☁️ Deploy no Vercel

### 1️⃣ Cria conta gratuita
👉 [https://vercel.com](https://vercel.com)

### 2️⃣ Faz upload dos ficheiros:
- `app.py`
- `requirements.txt`
- `vercel.json`
- Pasta `templates/`
- Pasta `static/`

### 3️⃣ Clica em **Deploy**

#### `requirements.txt` obrigatório:

```
Flask==3.0.3
yfinance==0.2.50
pandas==2.2.3
numpy==1.26.4
gunicorn==23.0.0
```

#### `vercel.json` obrigatório:

```json
{
  "builds": [
    { "src": "app.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "app.py" }
  ]
}
```

---

## 🧠 Indicadores Técnicos (Glossário)

| Sigla | Nome | Descrição |
|--------|------|------------|
| **RSI** | Relative Strength Index | Mede força do movimento (70 = sobrecompra, 30 = sobrevenda) |
| **EMA5 / EMA20** | Exponential Moving Average | Médias móveis exponenciais de curto e longo prazo |
| **Mom5** | Momentum 5 dias | Mede aceleração da variação de preço |
| **Vol10** | Volatilidade 10 dias | Mede instabilidade (%) |
| **Prob. IA** | Probabilidade de subida | Cálculo heurístico da IA |
| **Conf. IA** | Confiança IA | Grau de clareza da previsão |
| **Tendência** | Síntese final | Combina todos os sinais técnicos da IA |

---

## 🎨 Créditos

- Desenvolvido por **Rui Cirilo**  
- Visual futurista e IA desenvolvidos com **Flask + Chart.js + CSS Neon**  
- Dados de mercado obtidos via **Yahoo Finance**

---

## 📜 Licença

Projeto livre para uso educacional e pessoal.  
© 2025 — *Painel IA dos Mercados*
