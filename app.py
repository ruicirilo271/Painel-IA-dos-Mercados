import yfinance as yf
import numpy as np
import pandas as pd
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__, static_folder="static", template_folder="templates")

IA_HISTORY = []  # histórico IA para gráfico

# =====================================================
# 🔹 Função segura e compatível com o Vercel
# =====================================================
def safe_download(tickers):
    for t in tickers:
        try:
            print(f"🔹 A tentar {t}")
            df = yf.download(
                t,
                period="3mo",
                interval="1d",
                progress=False,
                auto_adjust=False,
                threads=False,
                timeout=5  # ⏱️ evita crash no Vercel
            )

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df.dropna(subset=["Close"])

            if df.empty:
                continue

            df["Close"] = df["Close"].astype(float)
            print(f"✅ OK {t} ({len(df)} registos)")
            return df

        except Exception as e:
            print(f"⚠️ Falha {t}: {e}")

    # 💾 fallback: dados simulados (modo offline)
    print("⚙️ Modo offline (simulação de dados)")
    dates = pd.date_range(end=datetime.now(), periods=30)
    df = pd.DataFrame({
        "Close": np.linspace(100, 110, len(dates)) + np.random.randn(len(dates))
    }, index=dates)
    return df

# =====================================================
# 📊 Indicadores técnicos
# =====================================================
def compute_indicators(df):
    df = df.copy()
    df["EMA5"] = df["Close"].ewm(span=5).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["Mom5"] = df["Close"].diff(5)
    df["Vol10"] = df["Close"].pct_change().rolling(10).std() * 100

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    return df

# =====================================================
# 🤖 IA simples
# =====================================================
def ai_predict(df):
    if len(df) < 2:
        return {"error": "Dados insuficientes"}

    last = df.iloc[-1]
    prev = df.iloc[-2]

    chg = float(last["Close"] / prev["Close"] - 1)
    mom = float(last["Mom5"])
    ema_fast = float(last["EMA5"])
    ema_slow = float(last["EMA20"])
    rsi = float(last["RSI"])
    vol = float(last["Vol10"])

    score = 0
    if chg > 0: score += 1
    if mom > 0: score += 1
    if ema_fast > ema_slow: score += 1
    if 40 < rsi < 60: score += 0.5
    elif rsi >= 60: score += 1
    if vol < 2: score += 0.5

    prob = min(100, (score / 4.5) * 100)
    conf = abs(50 - rsi) / 2

    decision = (
        "SUBIR" if prob > 55 else
        "DESCER" if prob < 45 else
        "NEUTRO"
    )
    color = (
        "#00ff99" if decision == "SUBIR" else
        "#ff5555" if decision == "DESCER" else
        "#ffff66"
    )
    comment = (
        "📈 Tendência de alta" if decision == "SUBIR" else
        "📉 Tendência de baixa" if decision == "DESCER" else
        "⚖ Tendência neutra"
    )

    return {
        "decision": decision,
        "decision_color": color,
        "prob": prob,
        "conf": conf,
        "comment": comment,
        "latest": {
            "rsi": round(rsi, 2),
            "ema_fast": round(ema_fast, 2),
            "ema_slow": round(ema_slow, 2),
            "mom5": round(mom, 4),
            "vol10": round(vol, 4),
        },
        "data": df["Close"].tail(30).astype(float).round(2).tolist(),
    }

# =====================================================
# 🌍 Rotas
# =====================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/snapshot")
def snapshot():
    print("\n🚀 Atualizando dados…")

    markets = {
        "Global": ["^GSPC", "^DJI", "^IXIC"],
        "Cripto": ["BTC-USD", "ETH-USD"],
        "Europa": ["^STOXX50E", "^FCHI"],
    }

    results = {}
    probs, confs = [], []

    for name, tickers in markets.items():
        print(f"\n🔎 A obter {tickers} …")
        df = safe_download(tickers)
        df = compute_indicators(df)

        ai = ai_predict(df)
        results[name] = ai
        if "error" not in ai:
            probs.append(ai["prob"])
            confs.append(ai["conf"])

    avg_prob = np.mean(probs) if probs else 0
    avg_conf = np.mean(confs) if confs else 0
    trend = (
        "🟢 Tendência geral: otimista" if avg_prob > 55 else
        "🔴 Tendência geral: negativa" if avg_prob < 45 else
        "⚪ Tendência geral: neutra"
    )

    IA_HISTORY.append({"time": datetime.now().strftime("%H:%M"), "prob": round(avg_prob, 2)})
    if len(IA_HISTORY) > 30:
        IA_HISTORY.pop(0)

    results["summary"] = {
        "trend": trend,
        "avg_prob": avg_prob,
        "avg_conf": avg_conf,
        "history": IA_HISTORY,
    }

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


