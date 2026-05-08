import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import streamlit as st
from streamlit.components.v1 import html
import tempfile
from matplotlib.animation import PillowWriter

st.set_page_config(page_title="Quantum Box", layout="wide")

st.title("Quantum Standing Wave in a 1D Box")

n = st.slider("Energy Level", 1, 6, 1)

L = 1
x = np.linspace(0, L, 1500)

fig, ax = plt.subplots(figsize=(14,6))

bg = '#0b0b12'
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

ax.plot([0,0],[-1.35,1.35], color='white', lw=10)
ax.plot([L,L],[-1.35,1.35], color='white', lw=10)

ax.plot([0,L],[1.2,1.2], color='white', lw=1, alpha=0.15)
ax.plot([0,L],[-1.2,-1.2], color='white', lw=1, alpha=0.15)

ax.plot([0,L],[0,0], color='white', lw=1.5, alpha=0.3)

ax.text(0,-1.45,'0', color='white', fontsize=14, ha='center')
ax.text(L,-1.45,'L', color='white', fontsize=14, ha='center')

ax.set_title(
    f'Quantum Standing Wave in a 1D Box   (n = {n})',
    fontsize=20,
    color='white',
    pad=20
)

if n == 1:
    wavelength_text = r'$L = \frac{\lambda}{2}$'
else:
    wavelength_text = rf'$L = \frac{{{n}\lambda}}{{2}}$'

ax.text(
    0.5,
    -1.42,
    wavelength_text,
    color='#ffd966',
    fontsize=20,
    ha='center'
)

nodes_x = np.linspace(0, L, n+1)

ax.scatter(
    nodes_x,
    np.zeros_like(nodes_x),
    color='#ff4d4d',
    s=120,
    zorder=5
)

for nx in nodes_x:
    ax.text(
        nx,
        -0.18,
        'Node',
        color='#ff6666',
        fontsize=11,
        ha='center'
    )

antinodes_x = (nodes_x[:-1] + nodes_x[1:]) / 2

antinode_points = ax.scatter(
    antinodes_x,
    np.sin(n*np.pi*antinodes_x/L),
    color='#66ff66',
    s=140,
    zorder=6
)

antinode_labels = []

for axx in antinodes_x:
    txt = ax.text(
        axx,
        0.8,
        'Antinode',
        color='#66ff66',
        fontsize=11,
        ha='center'
    )
    antinode_labels.append(txt)

ax.text(
    0.82,
    1.15,
    f'Energy ∝ n² = {n**2}',
    color='#cc99ff',
    fontsize=15
)

glow, = ax.plot([], [], lw=12, alpha=0.25, color='violet')
line, = ax.plot([], [], lw=4, color='cyan')

ax.set_xlim(-0.08,1.08)
ax.set_ylim(-1.6,1.6)

ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

def update(frame):

    t = frame / 18

    y = np.sin(n*np.pi*x/L) * np.cos(2*t)

    line.set_data(x, y)
    glow.set_data(x, y)

    line.set_color(
        plt.cm.cool((np.sin(t)+1)/2)
    )

    antinode_y = np.sin(n*np.pi*antinodes_x/L) * np.cos(2*t)

    antinode_points.set_offsets(
        np.c_[antinodes_x, antinode_y]
    )

    for i, txt in enumerate(antinode_labels):
        txt.set_position(
            (antinodes_x[i], antinode_y[i] + 0.15)
        )

    return line, glow, antinode_points

ani = FuncAnimation(
    fig,
    update,
    frames=200,
    interval=30,
    blit=True
)

gif_path = tempfile.NamedTemporaryFile(suffix=".gif", delete=False).name

ani.save(gif_path, writer=PillowWriter(fps=30))

st.image(gif_path)
