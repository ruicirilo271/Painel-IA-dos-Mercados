document.addEventListener("DOMContentLoaded", () => {
  const summaryEl = document.querySelector(".summary");
  const marketsContainer = document.querySelector(".markets-container");
  const loadingEl = document.querySelector(".loading");
  const audio = new Audio("/static/bip.mp3");
  const btnRefresh = document.getElementById("refreshButton");
  const iaChartEl = document.getElementById("iaChart");
  let iaChart = null;

  // 🔁 Atualiza previsões periodicamente
  async function loadSnapshot(playSound = true) {
    loadingEl.style.display = "block";
    marketsContainer.innerHTML = "";
    summaryEl.innerHTML = "<p>🤖 A IA está a analisar os mercados...</p>";

    try {
      const res = await fetch("/api/snapshot");
      if (!res.ok) throw new Error("Erro ao obter dados da API.");
      const data = await res.json();

      if (playSound) audio.play().catch(() => {});

      // 🧩 Resumo da IA
      summaryEl.innerHTML = `
        <h2>${data.summary.trend}</h2>
        <p>📈 Probabilidade média de subida: ${data.summary.avg_prob.toFixed(1)}%</p>
        <p>🧠 Confiança média: ${data.summary.avg_conf.toFixed(1)}%</p>
      `;

      // 🌈 Atualiza gráfico histórico da IA
      const labels = data.summary.history.map(p => p.time);
      const probs = data.summary.history.map(p => p.prob);

      if (iaChart) iaChart.destroy();
      iaChart = new Chart(iaChartEl, {
        type: "line",
        data: {
          labels,
          datasets: [{
            label: "Histórico da IA (%)",
            data: probs,
            borderColor: "#00ffff",
            borderWidth: 3,
            fill: true,
            backgroundColor: "rgba(0,255,255,0.07)",
            tension: 0.35,
          }]
        },
        options: {
          animation: { duration: 1500, easing: "easeInOutQuart" },
          plugins: { legend: { display: false } },
          scales: {
            y: { min: 0, max: 100, grid: { color: "#00ffff22" }, ticks: { color: "#00fff2" } },
            x: { grid: { color: "#00ffff11" }, ticks: { color: "#00fff2" } }
          }
        }
      });

      // 🏦 Cria cards de cada mercado
      for (const [key, market] of Object.entries(data)) {
        if (key === "summary") continue;
        if (!market.latest) continue;

        const { latest } = market;
        const card = document.createElement("div");
        card.className = "market-card";
        card.innerHTML = `
          <h3>${key}</h3>
          <div class="trend" style="color:${market.decision_color}">
            ${market.decision} (${market.prob.toFixed(1)}%)
          </div>
          <p class="comment">${market.comment}</p>
          <div class="indicators">
            <div><b>RSI:</b> ${latest.rsi}</div>
            <div><b>EMA5:</b> ${latest.ema_fast}</div>
            <div><b>EMA20:</b> ${latest.ema_slow}</div>
            <div><b>Mom5:</b> ${latest.mom5}</div>
            <div><b>Vol10:</b> ${latest.vol10}</div>
          </div>
          <canvas id="${key}-chart"></canvas>
        `;
        marketsContainer.appendChild(card);

        // 🔹 Pequeno gráfico individual
        const ctx = document.getElementById(`${key}-chart`);
        new Chart(ctx, {
          type: "line",
          data: {
            labels: Array(market.data.length).fill(""),
            datasets: [{
              data: market.data,
              borderColor: market.decision_color,
              borderWidth: 2,
              fill: false,
              tension: 0.25
            }]
          },
          options: {
            responsive: true,
            scales: {
              x: { display: false },
              y: { display: false }
            },
            plugins: { legend: { display: false } },
            elements: { point: { radius: 0 } }
          }
        });
      }

      loadingEl.style.display = "none";
    } catch (err) {
      console.error("❌ Erro:", err);
      summaryEl.innerHTML = "<p>⚠ Erro ao carregar dados.</p>";
    }
  }

  // 🔘 Botão de atualização manual
  btnRefresh.addEventListener("click", () => {
    btnRefresh.classList.add("active");
    loadSnapshot(true).then(() => {
      setTimeout(() => btnRefresh.classList.remove("active"), 800);
    });
  });

  // 🌐 TOOLTIP IA — sempre por cima de tudo
  const tooltip = document.createElement("div");
  tooltip.id = "tooltip-global";
  Object.assign(tooltip.style, {
    position: "fixed",
    background: "rgba(0,255,255,0.95)",
    color: "#000",
    padding: "8px 12px",
    borderRadius: "6px",
    boxShadow: "0 0 12px rgba(0,255,255,0.6)",
    fontSize: "0.9em",
    pointerEvents: "none",
    opacity: "0",
    transition: "opacity 0.2s, transform 0.2s",
    zIndex: "999999"
  });
  document.body.appendChild(tooltip);

  document.querySelectorAll(".term").forEach(el => {
    el.addEventListener("mouseenter", e => {
      tooltip.textContent = el.getAttribute("data-tooltip");
      tooltip.style.opacity = "1";
      tooltip.style.transform = "translateY(-8px)";
    });
    el.addEventListener("mousemove", e => {
      tooltip.style.left = e.clientX + 15 + "px";
      tooltip.style.top = e.clientY - 20 + "px";
    });
    el.addEventListener("mouseleave", () => {
      tooltip.style.opacity = "0";
    });
  });

  // 🚀 Primeira carga + atualização automática
  loadSnapshot(false);
  setInterval(() => loadSnapshot(false), 60000);
});
