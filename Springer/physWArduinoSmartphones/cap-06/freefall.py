import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations as comb

def averageSlope(x, y):
    ijpairs = list(comb(np.arange(len(y)), 2))
    m = 0
    m2 = 0
    for ij in ijpairs:
        i = ij[0]
        j = ij[1]
        s = (y[i]-y[j])/(x[i]-x[j])
        m += s
        m2 += s*s
    N = len(ijpairs)
    m /= N    
    sigma = np.sqrt(m2/N-m*m)
    return m, sigma

def averageIntercept(x, y, slope):
    vbeta = []
    for i in range(len(x)):
        vbeta.append(y[i]-slope*x[i])
    beta = np.mean(vbeta)
    dbeta = np.std(vbeta)
    return beta, dbeta

def truncatedMeasurement(m, sigma):
    e = np.floor(np.log(np.abs(sigma))/np.log(10))
    mprime = np.round(m/10**e,0)*10**e
    return mprime

if len(sys.argv) <= 1:
    print('Usage: freefall.py [filename]')
else:
    f = pd.read_csv(sys.argv[1])
    data = f.T.values.tolist()
    x = data[0]
    y = data[1]

    print('========== simple linear model')
    fig = plt.figure(figsize=(8.5,4))
    plt.plot(x, y, 'o')
    plt.xlabel('h [m]')
    plt.ylabel('t [s]')
    plt.show()
    m, sigma = averageSlope(x, y)
    alpha = truncatedMeasurement(m, sigma)
    print('Slope = {} +- {} ({})'.format(m, sigma, alpha))
    beta, dbeta = averageIntercept(x, y, alpha)
    betat = truncatedMeasurement(beta, dbeta)
    print('Beta = {} +- {} ({})'.format(beta, dbeta, betat))

    fig = plt.figure(figsize=(8.5,4))
    xrange = np.arange(0., 1.1, .001)
    plt.plot(x, y, 'o')
    model = alpha * xrange + beta
    plt.plot(xrange, model, '-r')
    plt.xlabel('h [m]')
    plt.ylabel('t [s]')
    plt.xlim(0., 1.1)
    plt.ylim(0., 0.5)
    plt.plot(xrange, np.sqrt(2*xrange/9.8), '-g')
    plt.show()

    print('========== linearised model')
    fig = plt.figure(figsize=(8.5,4))
    t2 = [t*t for t in y]
    plt.plot(x, t2, 'o')
    plt.xlabel('h [m]')
    plt.ylabel('t$^2$ [s$^2$]')
    plt.show()
    m, sigma = averageSlope(x, t2)
    alpha = truncatedMeasurement(m, sigma)
    print('Slope = {} +- {} ({})'.format(m, sigma, alpha))
    beta, dbeta = averageIntercept(x, t2, alpha)
    betat = truncatedMeasurement(beta, dbeta)
    print('Beta = {} +- {} ({})'.format(beta, dbeta, betat))

    model = alpha * xrange + beta
    plt.plot(x, t2, 'o')
    plt.xlim(0., 1.1)
    plt.ylim(0., 0.5)
    plt.plot(xrange, model, '-r')
    plt.xlabel('h [m]')
    plt.ylabel('t$^2$ [s$^2$]')
    plt.show()

    print('========== corrected model')
    fig = plt.figure(figsize=(8.5,4))
    t2c = []
    for i in range(len(x)):
        tc = y[i]+x[i]/340-float(sys.argv[2])
        t2c.append(tc*tc)
    plt.plot(x, t2c, 'o')
    plt.xlabel('h [m]')
    plt.ylabel('t$^2_{corr}$ [s$^2$]')
    plt.show()
    m, sigma = averageSlope(x, t2c)
    alpha = truncatedMeasurement(m, sigma)
    print('Slope = {} +- {} ({})'.format(m, sigma, alpha))
    beta, dbeta = averageIntercept(x, t2c, alpha)
    betat = truncatedMeasurement(beta, dbeta)
    print('Beta = {} +- {} ({})'.format(beta, dbeta, betat))

    model = alpha * xrange + beta
    plt.plot(x, t2c, 'o')
    plt.xlim(0., 1.1)
    plt.ylim(0., 0.5)
    plt.plot(xrange, model, '-r')
    plt.xlabel('h [m]')
    plt.ylabel('t$^2_{corr}$ [s$^2$]')
    plt.show()

    
