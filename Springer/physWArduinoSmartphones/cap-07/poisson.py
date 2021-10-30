import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

i = 1
binwidth = 1
plt.figure(figsize=(8.5,4))
while i < 30:
    x = np.random.poisson(i, 100000)
    plt.hist(x, histtype = 'step', rwidth=1,
             bins=range(min(x), max(x) + binwidth, binwidth),
             label='M = {}'.format(i))
    i *= 3
    
plt.xlim(0,50)
plt.legend()
plt.show()

Ntot = 9749
N = 4728
M = Ntot * 0.5
print('N = {}'.format(Ntot))
print('Expected value: {:.0f} +- {:.0f}'.
      format(M, np.sqrt(M)))
print('Observed value: {:.0f} +- {:.0f}'.
      format(N, np.sqrt(N)))
d = np.fabs(M-N)
sd = np.sqrt(M+N)
print('Difference    : {:.0f} +- {:.0f}'.
      format(d, sd))
P = poisson.pmf(N, M)
C = poisson.cdf(N, M)
print('P({:.0f}, {:.0f}) = {:.2e}'.
      format(N, M, P))
print('C({:.0f}) = '.format(N) + str(C))

