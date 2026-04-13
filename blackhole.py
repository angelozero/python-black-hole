import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

# --- Configurações Físicas ---
rs = 1.0            # Raio de Schwarzschild
distancia_ini = 20.0
n_raios = 18

def deriv(u_phi, phi, rs):
    u, p = u_phi
    return [p, 1.5 * rs * u**2 - u]

# --- Pré-processamento das Trajetórias ---
trajetorias = []
impactos = np.linspace(-5.0, 5.0, n_raios)

for b in impactos:
    if abs(b) < 0.1: b = 0.1
    # Usamos um range de phi bem grande para capturar as voltas
    phi_span = np.linspace(np.pi, -5 * np.pi, 2000) 
    u0 = 1.0 / distancia_ini
    p0 = -np.sqrt(np.abs(1.0/b**2 - (1.0 - rs/distancia_ini) * u0**2))
    
    sol = odeint(deriv, [u0, p0], phi_span, args=(rs,))
    r = 1.0 / sol[:, 0]
    
    # Converter para cartesianas
    x = r * np.cos(phi_span)
    y = r * np.sin(phi_span)
    
    # Filtrar apenas pontos que fazem sentido visual (não cruzar o centro)
    mask = r > rs * 0.8
    x, y = x[mask], y[mask]
    
    # Calcular a cor baseada na aproximação máxima
    cor = '#ff9100' if np.min(r) < 1.05 * rs else '#00ccff'
    
    trajetorias.append({'x': x, 'y': y, 'color': cor})

# --- Configuração do Gráfico ---
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.axis('off')

# Desenhar Buraco Negro
ax.add_patch(plt.Circle((0, 0), rs, color='black', zorder=10))
ax.add_patch(plt.Circle((0, 0), 1.5*rs, color='red', fill=False, ls='--', alpha=0.2))

# Estrelas estáticas
ex = np.random.uniform(-15, 15, 150)
ey = np.random.uniform(-15, 15, 150)
ax.scatter(ex, ey, color='white', s=0.5, alpha=0.3)

# Inicializar linhas
linhas = [ax.plot([], [], color=t['color'], lw=1.2, alpha=0.8)[0] for t in trajetorias]

def update(frame):
    # 'frame' vai ditar quantos pontos da lista desenhamos
    # Multiplicamos por um fator para acelerar a animação
    idx = frame * 4 
    for i, t in enumerate(trajetorias):
        end = min(idx, len(t['x']))
        linhas[i].set_data(t['x'][:end], t['y'][:end])
    return linhas

# Criar animação
# Usamos frames o suficiente para cobrir o maior array de trajetória
max_len = max(len(t['x']) for t in trajetorias) // 4
ani = FuncAnimation(fig, update, frames=max_len, interval=20, blit=True)

plt.title("Simulação Física: Luz em torno do Buraco Negro", color='white', pad=20)

# print("Salvando GIF... aguarde.")
# ani.save('blackhole.gif', writer='pillow', fps=30)
# print("GIF salvo com sucesso!")


plt.show()

