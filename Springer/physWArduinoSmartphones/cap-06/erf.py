import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.special import erf

x = np.arange(-5, 5, .01)
y = norm(0., 1.)
plt.plot(x, y.pdf(x), '-')
plt.plot(x, y.cdf(x), '-')
plt.plot(x, erf(x), '-')
plt.show()
