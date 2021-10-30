import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

i = 1
binwidth = 1
plt.figure(figsize=(8.5,4))
while i < 40:
    x = np.random.binomial(100, i*1e-2, 100000)
    plt.hist(x, histtype = 'step', rwidth=1,
             bins=range(min(x), max(x) + binwidth, binwidth),
             label='p = {}'.format(i*1e-2))
    i += 10
    
plt.xlim(0,50)
plt.legend()
plt.show()

P = binom.pmf(4728, 10000, 0.5)
C = binom.cdf(4728, 10000, 0.5)
print('P(4728; N=10000, p=0.5) = {:.2e}'.format(P))
print('sum_{n=0}^{n=4728}P(4728; N=10000, p=0.5) = ' + str(C))

print('Examples of formatting')
print('n = {:d}'.format(10000))
print('n = {:8d}'.format(10000))
print('s = {:s}'.format('test'))
print('x = {:f}'.format(np.exp(1)))
print('x = {:.3f}'.format(np.exp(1)))
print('x = {:8.4f}'.format(np.exp(1)))
print('x = {:5.1e}'.format(np.exp(1)))
