import matplotlib.pyplot as plt
import numpy as np

x = []

for i in range(10000):
    x.append(np.random.uniform())

fig = plt.figure(figsize=(8.5,4))
plt.hist(x)
mux = np.mean(x)
sigmax = np.std(x)
print('mean = {} stdev = {}'.format(mux, sigmax))
plt.show()

x = np.random.uniform(size=10000)
fig = plt.figure(figsize=(8.5,4))
plt.hist(x, rwidth=0.9)
mux = np.mean(x)
sigmax = np.std(x)
print('mean = {} stdev = {}'.format(mux, sigmax))
plt.show()

x = np.random.uniform(low=-1, high=1, size=10000)
fig = plt.figure(figsize=(8.5,4))
plt.hist(x, rwidth=0.9, bins=50, density=True, color='green')
mux = np.mean(x)
sigmax = np.std(x)
print('mean = {} stdev = {}'.format(mux, sigmax))
plt.show()


