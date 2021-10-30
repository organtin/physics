import numpy as np
import matplotlib.pyplot as plt

N = 100

def distance(N):
    d = 0
    for i in range(N):
        dy = 1
        if np.random.uniform() > 0.5:
            dy = -1
        d  += dy
    return d

def simulate(n):
    y  = []
    for k in range(100):
        y.append(distance(n))
    return np.mean(y), np.std(y)

nsteps = 1
n = []
t = []
st = []
for k in range(10):
    ymean, sigma = simulate(nsteps)
    n.append(nsteps)
    t.append(ymean)
    st.append(sigma)
    nsteps *= 2

plt.figure(figsize=(8.5,4))
plt.errorbar(n, t, fmt = 'o', yerr = st, label = 'Average distance travelled')
plt.plot(n, st, 'o', label = 'Width of distance distribution')
plt.plot(n, np.sqrt(n), '-', label = '$y = \\sqrt{N}$')
plt.plot(n, [0]*len(n), '-', label = '$y = 0$')
plt.xlabel('$N$')
plt.ylabel('$y$')
plt.legend()
plt.show()

