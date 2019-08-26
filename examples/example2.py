import numpy as np
import matplotlib.pyplot as pl
import matplotlib.animation as animation
import region_plot as rp

def animate(v=0):
    def pred(x, y):
        return np.sin(x*x) + 3*y*y <= 1
    sp = pl.subplot(1, 2, 1)
    pl.title("$\sin(x^2)+3y^2 \leq 1\,\,(\\mathrm{discovery}=0.01)$", fontsize=14)
    rp.region_plot(pred, (-2, 2), (-2, 2), discovery = 0.01, nof_subdivisions=v, show_all=True, edgecolor="#000000", facecolor="#9090FF", alpha=0.5)
    pl.xlabel("$x$", fontsize=14)
    pl.ylabel("$y$", fontsize=14)
    sp = pl.subplot(1, 2, 2)
    rp.region_plot(pred, (-2, 2), (-2, 2), discovery = 0.1, nof_subdivisions=v, show_all=True, edgecolor="#000000", facecolor="#9090FF", alpha=0.5)
    pl.xlabel("$x$", fontsize=14)
    pl.ylabel("$y$", fontsize=14)
    pl.title("$\sin(x^2)+3y^2 \leq 1\,\,(\\mathrm{discovery}=0.1)$", fontsize=14)

fig = pl.figure(figsize=(12, 6))
ani = animation.FuncAnimation(fig, animate, frames=200)
ani.save("example2.mp4")

