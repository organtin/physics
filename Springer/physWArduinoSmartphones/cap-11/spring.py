import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

def spring(x, b, A, tau, omega, t0):
    C = 1/(4*tau**2)-omega**2
    S = omega/tau
    t = x-t0
    y = b + A*np.exp(-t/(2*tau))*(C*np.cos(omega*t) + S*np.sin(omega*t))
    return y

def computeChi2(y, f, e, dof):
    chi2 = 0
    i = 0
    y = y.to_list()
    f = f.to_list()
    e = e.to_list()
    for i in range(len(y)):
        chi2 += ((y[i]-f[i])/e[i])**2
    return chi2

f = pd.read_csv('rawdata-930g-c.csv', usecols=['Time (s)', 'Acceleration y (m/s^2)'])
print(f.columns)
t = f['Time (s)']
a = f['Acceleration y (m/s^2)']

plt.figure(figsize=(8.5,4))
plt.plot(t, a, 'o')
plt.xlabel('t [s]')
plt.ylabel('a [m/s$^2$]')
plt.show()

N = 5
t = t.groupby(t.index // N).mean()
e = a.groupby(a.index // N).std() / np.sqrt(N)
a = a.groupby(a.index // N).mean()

plt.figure(figsize=(8.5,4))
plt.errorbar(t, a, yerr = e, fmt = 'o')
plt.xlabel('t [s]')
plt.ylabel('a [m/s$^2$]')
plt.show()

p, pdict  = find_peaks(a)
print('==== peaks found at ====')
print(t[p])

A      = []
tau    = []
omega  = []
Aw     = []
tauw   = []
omegaw = []

for k in range(len(p) - 1):
    p0 = [0., 0.04, 1., 7.5, 0.]   
    res, cov = curve_fit(spring, t[p[k]:], a[p[k]:], sigma = e[p[k]:], p0=p0, maxfev=100000)
    s = spring(t[p[k]:], res[0], res[1], res[2], res[3], res[4])
    ndf = len(a[p[k]:])-len(res)
    chisq = computeChi2(a[p[k]:], s, e[p[k]:], ndf)
    print('Fit chi^2 = {} chi^2/NDF = {}'.format(chisq, chisq/ndf))
    print('b = {}  A = {}  tau = {}  omega = {} t0 = {}'.format(res[0], res[1], res[2], res[3], res[4]))
    print('errors: {} {} {} {} {}'.format(np.sqrt(cov[0][0]), np.sqrt(cov[1][1]), np.sqrt(cov[2][2]),
                                          np.sqrt(cov[3][3]), np.sqrt(cov[4][4])))
    A.append(np.fabs(res[1])/cov[1][1])
    tau.append(res[2]/cov[2][2])
    omega.append(res[3]/cov[3][3])
    Aw.append(1/cov[1][1])
    tauw.append(1/cov[2][2])
    omegaw.append(1/cov[3][3])
    
    plt.figure(figsize=(8.5,4))
    plt.errorbar(t[p[0]:], a[p[0]:], e[p[0]:], fmt = 'o')
    plt.plot(t[p[k]:], spring(t[p[k]:], res[0], res[1], res[2], res[3], res[4]), '-')
    plt.xlabel('t [s]')
    plt.ylabel('a$_y$ [m/s$^2$]')
    figname = 'springs-fit-{}.png'.format(k)
    plt.savefig(figname)
    plt.show()

Am = np.sum(A)/np.sum(Aw)
taum = np.sum(tau)/np.sum(tauw)
omegam = np.sum(omega)/np.sum(omegaw)
print()
print('A = {:.3f} +- {:.3f} tau = {:.3f} +- {:.3f} omega = {:.3f} +- {:.3f}'.format(Am, np.sqrt(1/np.sum(Aw)),
                                                                                    taum, np.sqrt(1/np.sum(tauw)),
                                                                                    omegam, np.sqrt(1/np.sum(omegaw))))
    
