import pandas as pd
import numpy as np

data = pd.read_csv('trainFalling.17.2', header = None, delimiter = ' ')
print(data)

t = data[0].tolist()
x = data[1].tolist()
tx = [t*1e-6 for t in t]

import matplotlib.pyplot as plt

plt.figure(figsize = (8.5, 3.5))
plt.plot(tx, x, '-o')
plt.xlabel('t [s]')
plt.ylabel('d [cm]')
plt.show()

x.pop()
tx.pop()

plt.figure(figsize = (8.5, 3.5))
plt.plot(tx, x, '-o')
plt.xlabel('t [s]')
plt.ylabel('d [cm]')
plt.show()

t0 = tx[0]
x0 = x[-1]
for i in range(len(x)):
    tx[i] -= t0
    x[i] -= x0

v = []
a = []
for i in range(len(x) - 1):    
    v.append((x[i+1]-x[i])/(tx[i+1]-tx[i])/100.)

for i in range(len(x) - 2):
    a.append((v[i+1]-v[i])/(tx[i+1]-tx[i]))
    
t = tx.copy()
t.pop()

ta = t.copy()
ta.pop()

fig = plt.figure(figsize = (8.3, 3.5))
avt = fig.add_subplot(1,2,1)
aat = fig.add_subplot(1,2,2)
avt.plot(t, v, 'o')
avt.set_xlabel('t [s]')
avt.set_ylabel('v [m/s]')
aat.plot(ta, a, 'o')
aat.set_xlabel('t [s]')
aat.set_ylabel('a [m/s$^2$]')
plt.show()

print('========= acceleration ===========')
stdeva = np.std(a)
stdevv = np.std(v)
print('average(a) = {:.2f} stdev(a) = {:.2f} stdev(a)/sqrt(N) = {:.2f}'.format(np.average(a), 
                                                                   stdeva, 
                                                                   stdeva/np.sqrt(len(a))))

from scipy.optimize import curve_fit

def linear(x, A, B):
    return A*x+B

def chisquare(x, y, fun, par, sigma = None):
    chi2 = 0.
    for i in range(len(x)):
        s = 1
        if sigma:
            s = sigma[i]
        chi2 += ((y[i]-fun(x[i], par[0], par[1]))/s)**2
    return chi2

print('======== v fit results ============')
res, cov = curve_fit(linear, t, v)

print('alpha = {:.2f} +- {:.2f}'.format(res[0], np.sqrt(cov[0][0])))
print('beta  = {:.2f} +- {:.2f}'.format(res[1], np.sqrt(cov[1][1])))

chi2 = chisquare(t, v, linear, res)
ndf = len(t)-len(res)
print('chiSquare    : {:.3f}/{} NDF'.format(chi2, ndf))
print('chiSquare/NDF: {:.3f}'.format(chi2/ndf))

from scipy import stats

print('p-value.     : {}'.format(1-stats.chi2.cdf(chi2, ndf)))

wv = [0.1*np.average(v)]*len(v)
wa = [0.2*np.average(a)]*len(a)

print('======== v weighted fit results ============')
fitres, cov = curve_fit(linear, t, v, sigma=wv, absolute_sigma=True)
print('** alpha = {:.2f} +- {:.2f}'.format(fitres[0], np.sqrt(cov[0][0])))
print('** beta  = {:.2f} +- {:.2f}'.format(fitres[1], np.sqrt(cov[1][1])))
chi2 = chisquare(t, v, linear, fitres, wv)
ndf = len(t)-len(fitres)
print('** chiSquare    : {:.2f}/{} NDF'.format(chi2, ndf))
print('** chiSquare/NDF: {:.2f}'.format(chi2/ndf))
print('** p-value      : {}'.format(1-stats.chi2.cdf(chi2, ndf)))

def constant(x, A):
    return A

print('======== a weighted fit results ============')
ares, cov = curve_fit(constant, ta, a, sigma=wa, absolute_sigma=True)
print('** a = {:.2f} +- {:.2f}'.format(ares[0], np.sqrt(cov[0][0])))
pp = [0, ares[0]]
chi2 = chisquare(ta, a, linear, pp, wa)
ndf = len(t)-len(ares)
print('** chiSquare    : {:.2f}/{} NDF'.format(chi2, ndf))
print('** chiSquare/NDF: {:.2f}'.format(chi2/ndf))
print('** p-value      : {}'.format(1-stats.chi2.cdf(chi2, ndf)))

print('======== a weighted fit (linear) results ============')
res, cov = curve_fit(linear, ta, a, sigma=wa, absolute_sigma=True)
print(res)
chi2 = chisquare(ta, a, linear, res, wa)
ndf = len(t)-len(res)
print('** chiSquare    : {:.2f}/{} NDF'.format(chi2, ndf))
print('** chiSquare/NDF: {:.2f}'.format(chi2/ndf))
print('** p-value      : {}'.format(1-stats.chi2.cdf(chi2, ndf)))

fig = plt.figure(figsize = (8.3, 3.5))
avt = fig.add_subplot(1,2,1)
aat = fig.add_subplot(1,2,2)
avt.errorbar(t, v, yerr = wv, fmt = 'o')

p2 = np.poly1d(fitres)

avt.plot(t, p2(t), '-')
avt.set_xlabel('t [s]')
avt.set_ylabel('v [m/s]')

ares, cov = curve_fit(constant, ta, a, sigma=wa)
sigma_a = np.sqrt(cov[0][0])
p2 = np.poly1d(ares)

tt = [ta[0]-0.1, ta[-1]+0.1]
aat.fill_between(tt, p2(tt)-stdeva, p2(tt)+stdeva, alpha=.25, hatch='///', edgecolor='red', facecolor='white')
aat.fill_between(tt, p2(tt)-2*sigma_a, p2(tt)+2*sigma_a, color = 'yellow')
aat.fill_between(tt, p2(tt)-sigma_a, p2(tt)+sigma_a, color = 'lightgreen')
aat.errorbar(ta, a, yerr = wa, fmt = 'o')
aat.set_xlim(tt[0], tt[-1])
aat.set_xlabel('t [s]')
aat.set_ylabel('a [m/s$^2$]')
plt.show()

