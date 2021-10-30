import matplotlib.pyplot as plt
import numpy as np

def gauss(x, mu, sigma):
    return np.exp(-0.5*((x-mu)/sigma)**2)/(np.sqrt(2*np.pi)*sigma)

fig = plt.gcf()

def plot(mu2):
    x = np.arange(0, 10, .1)
    y = gauss(x, 1, 1)*gauss(x, mu2, 1)
    M = np.max(y)*0.2
    label = '$\\mu_1=1;\\,\\mu_2={}$'.format(mu2)
    plt.plot(x, y, label = label)
    plt.legend()
    mu = (1+mu2)/2
    arr = dict(facecolor='blue')
    plt.annotate('$\\mu_1 = 1$', xy = (1, 0.),
                 ha = 'center',
                 xytext = (1, M), arrowprops = arr)
    plt.annotate('$\\mu_2 = {}$'.format(mu2),
                 xy = (mu2, 0.), ha = 'center',
                 xytext = (mu2, M), arrowprops = arr)
    arr = dict(facecolor='orange')
    plt.annotate('$\\mu = {}$'.format(mu),
                 xy = (mu, M/0.2*0.95),
                 xytext = (mu, M/0.2*0.70),
                 arrowprops = arr, ha = 'center')
    return plt

mu2 = 1
while mu2 < 20:
    plot(mu2)
    plt.pause(0.5)
    fig.clf()
    fig.canvas.draw()
    mu2 += 1

plt.figure(figsize=(8.5,4))
plot(6)
plt.savefig('product-of-gaussians.png')
