import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plotNormal(xmin, xmax, C, mu, sigma, plot):
    gauss = []
    x = np.arange(xmin, xmax, (xmax-xmin)/500)
    for i in range(500):
        gauss.append(C*np.exp(-0.5*((x[i]-mu)/sigma)**2))
    plot.plot(x, gauss, '-')
    return plot

if len(sys.argv) <= 1:
    print('Usage: acceleration.py [filename]')
else:
    f = pd.read_csv(sys.argv[1])
    data = f.T.values.tolist()
    t  = data[0]
    ax = data[1]
    ay = data[2]
    az = data[3]
    a  = data[4]

    fig = plt.figure(figsize=(8.5,4))
    plt.hist(ax)
    mux = np.mean(ax)
    sigmax = np.std(ax)
    print('ax = {} +- {}'.format(mux, sigmax))
    bw = (max(ax)-min(ax))/10
    C = len(ax)*bw
    C /= np.sqrt(2*np.pi)*sigmax
    plt = plotNormal(min(ax), max(ax), C, mux, sigmax, plt)
    plt.xlabel('a$_x$ [m/s$^2$]')
    plt.annotate('$\\langle a_x\\rangle$',
                 xy=(mux, C*0.05),
                 color='white',
                 xytext=(mux, C*0.55),
                 arrowprops=dict(ec='orange', arrowstyle='-|>', lw=4),
                 horizontalalignment='center',
                 verticalalignment='bottom')
    plt.show()

    fig = plt.figure(figsize=(8.5,4))
    plt.hist(ay)
    muy = np.mean(ay)
    sigmay = np.std(ay)
    print('ay = {} +- {}'.format(muy, sigmay))
    bw = (max(ax)-min(ax))/10
    C = len(ax)*bw
    C /= np.sqrt(2*np.pi)*sigmax
    plt = plotNormal(min(ay), max(ay), C, muy, sigmay, plt)
    plt.xlabel('a$_y$ [m/s$^2$]')
    plt.annotate('$\\sigma_y$', xy=(muy, C*0.65), textcoords='data', color='white')
    plt.annotate('',
                 xy=(muy-sigmay, C*0.6),
                 xytext=(muy+sigmay, C*0.6),
                 arrowprops=dict(ec='orange', arrowstyle='<|-|>', lw=4))
    plt.annotate('',
                 xy=(muy-sigmay, 0),
                 xytext=(muy-sigmay, C),
                 arrowprops={'arrowstyle': '-', 'ls': 'dashed'})
    plt.annotate('',
                 xy=(muy+sigmay, 0),
                 xytext=(muy+sigmay, C),
                 arrowprops={'arrowstyle': '-', 'ls': 'dashed'})    
    plt.show()

    fig = plt.figure(figsize=(8.5,4))
    plt.hist(az)
    muz = np.mean(az)
    sigmaz = np.std(az)
    print('az = {} +- {}'.format(muz, sigmaz))
    bw = (max(ax)-min(ax))/10
    C = len(ax)*bw
    C /= np.sqrt(2*np.pi)*sigmax
    plt = plotNormal(min(az), max(az), C, muz, sigmaz, plt)
    plt.xlabel('a$_z$ [m/s$^2$]')
    plt.show()

    fig = plt.figure(figsize=(8.5,4))
    plt.hist(a)
    mu = np.mean(a)
    sigma = np.std(a)
    print('a  = {} +- {}'.format(mu, sigma))
    print('estimated sigma_a = {}'.format(np.sqrt((mux/mu*sigmax)**2+(muy/mu*sigmay)**2+(muz/mu*sigmaz)**2)))
    bw = (max(ax)-min(ax))/10
    C = len(ax)*bw
    C /= np.sqrt(2*np.pi)*sigmax
    plt = plotNormal(min(a), max(a), C, mu, sigma, plt)
    plt.xlabel('a = $\sqrt{a_x^2+a_y^2+a_z^2}$ [m/s$^2$]')    
    plt.show()
