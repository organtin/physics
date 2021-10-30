import numpy as np
import matplotlib.pyplot as plt

n = 10000
N = 10000

avg = []
x = np.random.randint(1, 7, size = n)
m = np.mean(x)
s = np.std(x)
print('mu = {} sigma = {}'.format(m,s))
plt.figure(figsize=(8.5,4))
plt.hist(x, bins = range(1, 8), rwidth = 0.9)
plt.xlabel('$x$')
plt.show()

for i in range(N):
    x = np.random.randint(1, 7, size = n)
    m = np.mean(x)
    avg.append(m)

m = np.mean(avg)
s = np.std(avg)
print('mu = {} sigma = {}'.format(m,s))
plt.figure(figsize=(8.5,4))
plt.hist(avg, rwidth = 0.9)
plt.xlabel('$\\langle x\\rangle$')
plt.show()

