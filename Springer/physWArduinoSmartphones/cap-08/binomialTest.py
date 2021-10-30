import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.stats import binom
from scipy.stats import poisson

if len(sys.argv) <= 1:
    print('Usage: binomialTest.py [filename] [threshold]')
else:
    f = pd.read_csv(sys.argv[1])
    data = f.T.values.tolist()
    t  = data[0]
    ax = data[1]
    ay = data[2]
    az = data[3]
    a  = data[4]

threshold = float(sys.argv[2])
groupby = 40

mu = np.mean(ax)
sigma = np.std(ax)
ax = [(x - mu)/sigma for x in ax]
mu = np.mean(ay)
sigma = np.std(ay)
ay = [(x - mu)/sigma for x in ay]
mu = np.mean(az)
sigma = np.std(az)
az = [(x - mu)/sigma for x in az]
mu = np.mean(a)
sigma = np.std(a)
a = [(x - mu)/sigma for x in a]

ax += ay + az + a

random.shuffle(ax)

print('Data count: {}'.format(len(ax)))
print('Max       : {}'.format(max(ax)))
print('Min       : {}'.format(min(ax)))
N = len(ax) - groupby
k = 0
c = [0]*N
xmax = 0
xmin = N
while k < N:
    n = 0
    for i in range(groupby):
        if ax[i + k] > threshold:
            n += 1
    c[n] += 1
    if n > xmax:
        xmax = n
    if n < xmin:
        xmin = n
    k += groupby

x = range(int(xmax*1.1))
xmin = int(xmin * 0.9)
plt.bar(x[xmin:], c[xmin:len(x)])
i = 0
avg = 0
for i in x:
    avg += i*c[i]
avg /= np.cumsum(c)[-1]
plt.plot(x, np.cumsum(c)[-1]*binom.pmf(x, groupby, avg/groupby), color = 'orange')
plt.plot(x, np.cumsum(c)[-1]*poisson.pmf(x, avg), color='green')
plt.xlim(xmin, len(x))
plt.show()

