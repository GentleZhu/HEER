from plot_from_nparray import array_to_cdf
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

aw = np.load("../data/dblp_stats/dblp_jac_a_w.npz")
ay = np.load("../data/dblp_stats/dblp_jac_y_a.npz")
aw_x, aw_cum_y = array_to_cdf(aw["weighted"])
ay_x, ay_cum_y = array_to_cdf(ay["weighted"])

fig = plt.figure()

ax = fig.add_subplot(111)

#ax.plot(aw_x, aw_cum_y, 'r')
#ax.plot(ay_x, ay_cum_y, 'r--')
lns11 = ax.plot(aw_x, aw_cum_y, 'r', label = 'Authorship vs. Term usage', linewidth=2)
lns12 = ax.plot(ay_x, ay_cum_y, 'r--', label = 'Authorship vs. Publishing year', linewidth=2)


# added these three lines
lns = lns11+lns12
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

ax.grid()
#ax.set_xscale('log')
ax.set_xlabel(r"Generalized Jaccard coefficient", fontsize=16)
ax.set_xlim(0, 0.0004)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
ax.set_ylabel(r"CDF", fontsize=16)
ax.set_ylim(.0, 1.05)

plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.15)

plt.show()
