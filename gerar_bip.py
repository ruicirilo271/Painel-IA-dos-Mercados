import numpy as np
import soundfile as sf

# 🔊 Configuração do som
sample_rate = 44100  # Hz
duration = 0.45      # segundos
t = np.linspace(0, duration, int(sample_rate * duration), False)

# 🔮 Geração do tom (descida 1500Hz → 900Hz)
start_freq = 1500
end_freq = 900
freqs = np.linspace(start_freq, end_freq, len(t))
tone = np.sin(2 * np.pi * freqs * t)

# ✨ Aplicar curva de volume e eco digital
fade_out = np.linspace(1, 0, len(t))
tone *= fade_out

# Pequeno eco IA (delay de 60ms)
delay = int(0.06 * sample_rate)
echo = np.zeros_like(tone)
echo[delay:] = tone[:-delay] * 0.3
final = tone + echo

# Normalizar o áudio
final /= np.max(np.abs(final))

# 💾 Guardar o ficheiro MP3 futurista
sf.write("static/bip.mp3", final, sample_rate, format="OGG")  # OGG = leve e de alta qualidade
print("✅ Som futurista criado: static/bip.mp3")
