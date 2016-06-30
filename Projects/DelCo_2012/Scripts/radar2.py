import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

class Radar(object):

    def __init__(self, fig, titles, labels, rect=None):
        if rect is None:
            rect = [.05, .05, .95, .85]

        self.n = len(titles)
        self.angles = np.arange(90, 90+360, 360.0/self.n)
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) 
                         for i in range(self.n)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=titles, fontsize=14)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, 6), angle=angle, labels=label)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, 6)

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)



fig = plt.figure()
titles = list(["Straight Stream","Solid Stream","30$^{\circ}$ Fog"])
labels = [
    ["20", "40", "60", "80", "100"], 
    ["20", "40", "60", "80", "100"], 
    ["20", "40", "60", "80", "100"]
]

radar = Radar(fig, titles, labels)
radar.plot([55.5/20., 89.3/20., 65.2/20.],  "-", lw=2, color="b", linestyle='-', marker = 'o', alpha=0.4, label="Water")
radar.plot([50.1/20., 63.6/20., 47.4/20.],"-", lw=2, color="r", linestyle='-', marker = 's',  alpha=0.4, label="CAFS")
# radar.plot([3, 4, 2.9], "-",  lw=2, color="g", linestyle='-', marker = 'd', alpha=0.4, label="Class A")
radar.ax.legend()
plt.savefig('radar2.pdf',format='pdf')