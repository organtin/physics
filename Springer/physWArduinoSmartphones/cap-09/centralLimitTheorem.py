import numpy as np
import matplotlib.pyplot as plt

x = np.random.randint(1, 7, 10000)
plt.figure(figsize=(8.5,4))
plt.hist(x, bins = range(1,8), rwidth = 0.9)
plt.show()

y = np.random.randint(1, 7, 10000)
z = [x + y for x, y in zip(x, y)]
plt.figure(figsize=(8.5,4))
plt.hist(z, bins = range(2, 14), rwidth = 0.9)
plt.show()

def gaussian(x, mu, sigma):
    return np.exp(-0.5*((x-mu)/sigma)**2)/(np.sqrt(2*np.pi)*sigma)
    
x = []
for i in range(10):
    x.append(np.random.randint(1, 7, 10000))
z = [sum(i) for i in zip(*x)]
plt.figure(figsize=(8.5,4))
plt.hist(z, rwidth = 0.9)
plt.show()

x = []
for i in range(1000):
    x.append(np.random.randint(1, 7, 10000))
z = [sum(i) for i in zip(*x)]
#z = [sum(i) for i in zip(x[0], x[1], x[2], x[3], x[4],
#                         x[5], x[6], x[7], x[8], x[9])]
plt.figure(figsize=(8.5,4))
n, bins, patches = plt.hist(z, rwidth = 0.9)

binwidth = bins[1]-bins[0]
mu = 7*1000/2
sigma = np.sqrt(1000*6*6/12)
C = 10000*binwidth
x = np.arange(mu-4*sigma, mu+4*sigma)
plt.plot(x, C*gaussian(x, mu, sigma), '-', color='orange')
plt.show()

