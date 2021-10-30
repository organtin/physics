import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy import stats

def plotNormal(n, d, leg, plot):
    ran = []
    x = np.arange(-20*n, 20*n, 0.1)
    for i in range(10000):
        ran.append(np.array(np.sum(np.random.normal(0., 1., n)**d)))
    freq, bins, ni = plot.hist(ran, range(-20*n,20*n), histtype='step', label=leg)
    integral = np.sum(freq)
    if d == 1:
        plot.plot(x,stats.norm.pdf(x, 0., np.sqrt(n))*integral, '-', label=leg)
    if d == 2:
        plot.plot(x,stats.chi2.pdf(x, n)*integral, '-', label=leg)
    return plot

fig = plt.figure(figsize = (8.5, 3.5))
gaussians = fig.add_subplot(1,2,1)
chi2distr = fig.add_subplot(1,2,2)
gaussians = plotNormal(1, 1, '$\\nu=1$', gaussians)
gaussians = plotNormal(5, 1, '$\\nu=5$', gaussians)
gaussians = plotNormal(25, 1, '$\\nu=25$', gaussians)
gaussians.set_xlim(-20,20)
gaussians.legend(loc='upper right', shadow=False, fontsize='medium')

chi2distr = plotNormal(1, 2, '$\\nu=1$', chi2distr)
chi2distr = plotNormal(5, 2, '$\\nu=5$', chi2distr)
chi2distr = plotNormal(25, 2, '$\\nu=25$', chi2distr)
chi2distr.set_xlim(0,50)
chi2distr.set_ylim(0,3000)
chi2distr.legend(loc='upper right', shadow=False, fontsize='medium')
plt.savefig('../../figures/incline-gaussians.png')
plt.show()

plt.figure(figsize = (8.5, 3.5))
plt = plotNormal(100, 2, '$\\nu=100$', plt)
plt.xlim(0,200)
plt.ylim(0,400)
plt.savefig('../../figures/incline-chi2100.png')
plt.show()

