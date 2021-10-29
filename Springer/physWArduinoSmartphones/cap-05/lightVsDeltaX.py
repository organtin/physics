import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations as comb

C = 17.13
dx = 80e-6

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
    print('Usage: lightVsDeltaX.py [filename]')
else:
    f = pd.read_csv(sys.argv[1])
    data = f.T.values.tolist()
    x = [x*dx for x in data[0]]
    y = [x*C for x in data[1]]
    dy = [x*C for x in data[2]]

    xticks = np.arange(0, 1.0e-3, 1e-4) 

    print('========== simple linear model')
    fig = plt.figure(figsize=(8.5,4))
    plt.errorbar(x, y, yerr=dy, fmt='o')
    plt.title('Illuminance vs absorber thickness')
    plt.xlabel('x [m]')
    plt.ylabel('${\cal L}$ [lx]')
    plt.xticks(xticks)
    plt.show()
    m, sigma = averageSlope(x, y)
    alpha = truncatedMeasurement(m, sigma)
    print('Slope = {} +- {} ({})'.format(m, sigma, alpha))
    beta, dbeta = averageIntercept(x, y, alpha)
    betat = truncatedMeasurement(beta, dbeta)
    print('Beta = {} +- {} ({})'.format(beta, dbeta, betat))

    fig = plt.figure(figsize=(8.5,4))
    plt.errorbar(x, y, yerr=dy, fmt='o')
#    L = len(x)
#    A = np.zeros((L,L))
#    np.fill_diagonal(A, alpha)
#    B = np.full(L, beta)
#    model = np.matmul(A,x)+B
    model = [alpha * x + beta for x in x]
    plt.plot(x, model, '-r')
    plt.title('Illuminance vs absorber thickness')
    plt.xlabel('x [m]')
    plt.ylabel('${\cal L}$ [lx]')
    plt.xticks(xticks)
    plt.show()

    print('========== exponential model')
    dy_save = dy.copy()
    y_save = y.copy()

    for i in range(len(dy)):
        dy[i] = dy[i]/y[i]
    y0 = y[0]
    y = np.log(np.divide(y,y0))
    plt.errorbar(x, y, yerr=dy, fmt='o')
    plt.title('Illuminance vs absorber thickness')
    plt.xlabel('x [m]')
    plt.ylabel('$\\log{\\frac{{\\cal L}(x)}{{\\cal L}(0)}}$')
    plt.xticks(xticks)
    plt.show()
    m, sigma = averageSlope(x, y)
    alpha = truncatedMeasurement(m, sigma)
    print('Slope = {} +- {} ({})'.format(m, sigma, alpha))
    print('lambda = {}'.format(1/alpha))
    beta, dbeta = averageIntercept(x, y, alpha)
    betat = truncatedMeasurement(beta, dbeta)
    print('Beta = {} +- {} ({})'.format(beta, dbeta, betat))

    plt.errorbar(x, y, yerr=dy, fmt='o')
    L = len(x)
    A = np.zeros((L,L))
    np.fill_diagonal(A, alpha)
    B = np.full(L, beta)
    logmodel = np.matmul(A,x)+B
    plt.plot(x, logmodel, '-r')
    plt.title('Illuminance vs absorber thickness')
    plt.xlabel('x [m]')
    plt.ylabel('$\\log{\\frac{{\\cal L}(x)}{{\\cal L}(0)}}$')
    plt.xticks(xticks)
    plt.show()

    plt.errorbar(x, y_save, yerr=dy_save, fmt='o')
    plt.title('Illuminance vs absorber thickness')
    plt.xlabel('x [m]')
    plt.ylabel('${\\cal L}(x)$ [lx]')
    plt.xticks(xticks)
    expomodel = [y_save[0]*np.exp(m*z+beta)  for z in x]
    plt.plot(x, model, '-r')
    plt.plot(x, expomodel, '-g')
    plt.show()

#    vlog = np.vectorize(np.log)
#    velog = np.vectorize(elog)
#    ly = vlog(y)
#    ely = velog(y, dy)
#    plt.errorbar(x, ly, yerr=ely, fmt='o')
#    plt.show()
#    print(list(it.combinations(ly, 2)))
    
    
