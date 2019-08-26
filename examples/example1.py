import numpy as np
import matplotlib.pyplot as pl
import region_plot as rp

def example1():
    def pred(x, y):
        return np.sin(x*x) + 3*y*y <= 1
    pl.figure(figsize=(5, 5))
    rp.region_plot(pred, (-2, 2), (-2, 2), discovery=0.01, nof_subdivisions=5000, facecolor="#9090FF", alpha=0.5)
    pl.xlabel("$x$", fontsize=14)
    pl.ylabel("$y$", fontsize=14)
    pl.title("$\sin(x^2)+3y^2 \leq 1$", fontsize=14)
    pl.tight_layout()
    pl.savefig("example1.png")

example1()
