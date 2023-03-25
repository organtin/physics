#####################################################################################
#
#    ampere.py: analysis of the Ampere's Law experiment described in
#               P.Cicuta and G.Organtini, "A modern investigation of Ampere's Law"
#               Submitted to EJP
#    Copyright (C) 2023 Pietro Cicuta and Giovanni Organtini
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#####################################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.interpolate

SMARTPHONE = 0
ARDUINO = 1

plot = True # set to False to avoid doing plots

plt.rcParams.update({'font.size': 16})

def compute(datadir = '.', title = None, comp = 'y', offset = 0, fact = 1,
            setup = SMARTPHONE, verbose = False, plot = False):
    # compute the circulation of B
    wz = []
    By = []
    tg = []
    tm = []
    if setup == SMARTPHONE:
        magdata = pd.read_csv(f'{datadir}/Magnetometer.csv')
        gyrdata = pd.read_csv(f'{datadir}/Gyroscope.csv')
        tm = magdata['Time (s)']
        tg = gyrdata['Time (s)']
        By = magdata[f'Magnetic field {comp} (µT)']
        By = [fact*(B - offset) for B in By]
        wz = gyrdata['Gyroscope z (rad/s)']
    else:
        magdata = pd.read_csv(f'{datadir}')
        tm = magdata['t']
        tg = magdata['t']
        tm = [tm * 1e-6 for tm in tm]
        tg = [tg * 1e-6 for tg in tg]
        By = magdata['bx']
        wz = abs(magdata['w'])

    # interpolate data
    omega = scipy.interpolate.interp1d(tg, wz)
    magfield = scipy.interpolate.interp1d(tm, By)

    # check data: compute the angle and plot it, together with the angular
    #             velocity
    alpha = 0
    alphavec = []
    for i in range(len(tg) - 1):
        dt = tg[i+1] - tg[i]
        alpha += wz[i]*dt
        alphavec.append(alpha)

    if plot:
        fig, ax1 = plt.subplots()
        plt.subplots_adjust(bottom = 0.13, top = 0.95)
        color = 'tab:blue'
        ax1.plot(tg, wz, color = color)
        ax1.set_xlabel('t (s)')
        ax1.set_ylabel('$\\omega_z$ (rad/s)', color = color)
        color = 'tab:orange'
        ax2 = ax1.twinx()
        ax2.plot(tg[:-1], alphavec, color = color)
        ax2.set_ylabel('$\\alpha$ (rad)', color = color)    
        plt.show()

    i = 0
    kp = 0
    alpha = 0
    tt = []
    alphavec = []
    Bvec = []
    Bxvec = []
    Cvec = []
    C = 0
    n = 0
    dalphavec = []
    
    alphamin = .05

    # get the average dt
    dt = np.mean([t2-t1 for t1,t2 in zip(tm[:-1], tm[1:])])

    # integrate over the loop to get pseudo-circulation in T*urad
    for t in tm[1:-2]:
        dalpha = omega(t)*dt
        alpha += dalpha
        if (alpha > alphamin) and (alpha <= 2*np.pi+alphamin):
            dalphavec.append(dalpha)
            tt.append(t)
            alphavec.append(alpha)
            Bvec.append(magfield(t))
            C += magfield(t)*dalpha
            Cvec.append(C)
        n += 1

    # plot the magnetic field and the pseudo-circulation as a function of alpha
    if plot:
        fig, ax1 = plt.subplots()
        plt.subplots_adjust(bottom = 0.13, top = 0.95, left = 0.15, right = 0.85)
        color = 'tab:blue'
        ax1.plot(alphavec, Bvec, color = color)
        ax1.set_xlabel('$\\alpha$ [rad]')
        ax1.set_ylabel('$B_y$ [$\\mu$T]', color = color)
        ax2 = ax1.twinx()        
        color = 'tab:orange'
        ax2.plot(alphavec, Cvec, color = color)    
        ax2.set_ylabel('${\\cal C}$ [$\\mu$T$\\,$rad]', color = color)
        plt.annotate(title, xy=(.70, .85), xycoords = 'axes fraction')
        plt.show()

    if verbose:
        print(f'{title}\tC={C:.2f} [uT*rad]')
    return C

def arduino(file1, file2, I = 0, offset = 0, soffset = 0, r = 4.4e-2, sr = 0.3e-2,
            header = False):
    # get two data file taken with Arduino, compute the pseudo-circulation for both
    title = f'I = {I:.2f} A'
    C0 = compute(file1, title, setup = ARDUINO)
    C1 = compute(file2, title, setup = ARDUINO)
    # compute the average between the two and the standard deviation
    Cmean = (C0+C1)/2
    sCmean  = abs(C1-C0)/np.sqrt(12)
    # compute CNET
    Cnet = Cmean - offset
    sCnet = np.sqrt(sCmean**2 + soffset**2)
    # compute the circultation in uT*m and its uncertainty
    CC = Cnet * r
    sCC = np.sqrt((sCnet*r)**2 + (sr*Cnet)**2)

    if header:
        print(f'C0 [uT*rad] C1 [uT*rad] I [A]  C [uT*rad] Cnet [uT*rad] CC [uT*m]')
    print(f'{C0:11.2f} {C1:11.2f} {I:5.2f} {Cmean:5.2f}+-{sCmean:4.2f} ' +
          f'{Cnet:7.2f}+-{sCnet:4.2f} ' +
          f'{CC:4.2f}+-{sCC:4.2f}')
    return Cmean, sCmean

def smartphone(file1, file2, I = 0, conf = 'A', offset1 = 0, offset2 = 0, header = False,
               rtheta = None):
    title = f'I = {I:.2f} A'
    C1 = compute(file1, title, setup = SMARTPHONE)
    C2 = compute(file2, title, setup = SMARTPHONE)
    C1Net = C1
    C2Net = C2
    if offset1 != 0:
        C1Net -= offset1
    if offset2 != 0:
        C2Net -= offset2
    CC1 = 0
    CC2 = 0
    if rtheta != None:
        CC1 = C1*rtheta[0]/np.cos(rtheta[1])
        CC2 = C1*rtheta[2]/np.cos(rtheta[3])
    Cmean = (CC1+CC2)/2
    sCmean = abs(CC1-CC2)/np.sqrt(12) 
    if header:
        print(f'I [A] Conf. C1 [uT*rad] C2 [ut*rad] C1Net [ut*rad] [C2Net [uT*rad] ' +
              f'CC1 [uT*m] CC2[uT*m]    CC[uT*m]')
    print(f'{I:5.2f} {conf:>5} {C1:11.2f} {C2:11.2f} {C1Net:14.2f} {C2Net:14.2f} ' +
          f'{CC1:11.2f} {CC2:9.2f} {Cmean:4.2f}+-{sCmean:4.2f}')
    return C1Net, C2Net

from scipy.optimize import curve_fit

def line(x, m, q):
    return m*x+q

def getDistance(x, B0, B3, plot = False):
    Binv = [1/(B3-B0) for B3,B0 in zip(B3,B0)]
    p1, cov1 = curve_fit(line, x, Binv)
    
    if plot:
        plt.subplots_adjust(left = 0.2, bottom = 0.15)
        plt.plot(x, Binv, 'o')
        plt.plot([x[0], x[-1]], [line(x[0], p1[0], p1[1]), line(x[-1], p1[0], p1[1])], '-')
        plt.xlabel('r [cm]')
        plt.ylabel('1/B [$\\mu$T$^{-1}$]')
        plt.annotate('Phone ①', xy = (0.7, 0.9), xycoords = 'axes fraction')
        plt.savefig('BinvVsrPhone1.png')
        plt.show()
    return p1, cov1

# Adjust the following lists to contain data for the measurement of the sensor's position
# inside the smartphone: x contains the distances from the wire, B0 is the corresponding
# value when I=0, while B3 is the value of the magnetic field measured with I>0 (3 A in
# our case)

# data to get the distance of the sensor from the long side (phone 1)

x  = [0, 2, 3, 4]           # distances
B0 = [-36, -36, -36, -36]   # Earth's magnetic field
B3 = [-71, -56, -51, -48]   # magnetic field for 3A

p1, cov1 = getDistance(x, B0, B3)

# data to get the distance of the sensor from the long side (phone 2)

x  = [0, 2, 3, 4]          # distances
B0 = [-3, -16, -31, -27]   # Earth's magnetic field
B3 = [-45, -36, -47, -40]  # magnetic field for 3A

p2, cov2 = getDistance(x, B0, B3)

# data to get the distance of the sensor from the short side (phone 1)

x  = [0, 2, 3, 4]          # distances
B0 = [-30, -38, -42, -42]  # Earth's magnetic field
B3 = [-72, -57, -57, -55]  # magnetic field for 3A

p3, cov3 = getDistance(x, B0, B3)

# data to get the distance of the sensor from the short side (phone 2)

x  = [0, 2, 3, 4]          # distances
B0 = [-17, -18, -20, -19]  # Earth's magnetic field
B3 = [-85, -43, -37, -34]  # magnetic field for 3A

p4, cov4 = getDistance(x, B0, B3)

d1 = p1[1]/p1[0]
s0 = np.sqrt(cov1[0][0])
s1 = np.sqrt(cov1[1][1])
sd1 = np.sqrt((s1/p1[0])**2+(p1[1]*s0/p1[0]**2)**2)
print(f'd1 = {d1:.1f}+-{sd1:.1f} cm')
d2 = p2[1]/p2[0]
s0 = np.sqrt(cov2[0][0])
s1 = np.sqrt(cov2[1][1])
sd2 = np.sqrt((s1/p2[0])**2+(p2[1]*s0/p2[0]**2)**2)
print(f'd2 = {d2:.1f}+-{sd2:.1f} cm')
h1 = p3[1]/p3[0]
s0 = np.sqrt(cov3[0][0])
s1 = np.sqrt(cov3[1][1])
sh1 = np.sqrt((s1/p3[0])**2+(p3[1]*s0/p3[0]**2)**2)
print(f'h1 = {h1:.1f}+-{sh1:.1f} cm')
h2 = p4[1]/p4[0]
s0 = np.sqrt(cov4[0][0])
s1 = np.sqrt(cov4[1][1])
sh2 = np.sqrt((s1/p4[0])**2+(p4[1]*s0/p4[0]**2)**2)
print(f'h2 = {h2:.1f}+-{sh2:.1f} cm')

# Adjust the following data:
# rij represents the distances of the sensor i from the axis of rotation,
#     in configuration j, tij are the corresponding theta angles

# in configuration A

r1B = 10.5/100
r2B = 11.2/100
t1B = 66.75*np.pi/180
t2B = 68.59*np.pi/180

r1A = 4.7/100
r2A = 4.9/100
t1A = 24.73*np.pi/180
t2A = 33.31*np.pi/180

rtheta = [r1A, t1A, r2A, t2A]

# do the computation
# in our concentions IiNNxx, i=0 for no current in the wire, while i=1 if I>0;
# NN is just an arbitrary run identifier, xx identifies the phone

C1, C2 = smartphone('I030PC', 'I030GO', header = True, rtheta = rtheta)
smartphone('I131PC', 'I131GO', I = 2.13, offset1 = C1, offset2 = C2, rtheta = rtheta)
C1, C2 = smartphone('I032PC', 'I032GO', rtheta = rtheta)
smartphone('I133PC', 'I133GO', I = 2.13, offset1 = C1, offset2 = C2, rtheta = rtheta)
rtheta = [r1B, t1B, r2B, t2B]
C1, C2 = smartphone('I034PC', 'I034GO', conf = 'B', rtheta = rtheta)
smartphone('I135PC', 'I135GO', I = 2.13, offset1 = C1, offset2 = C2, conf = 'B',
           rtheta = rtheta)
rtheta = [r1A, t1A, r2A, t2A]
C1, C2 = smartphone('I036PC', 'I036GO', rtheta = rtheta)
smartphone('I137PC', 'I137GO', I = 1.11, offset1 = C1, offset2 = C2, rtheta = rtheta)

# do the calculation with Arduino
# in this case files are labelled as arduinoBi-j, where i is as above, while j
# is a unique run number
C0, sC0 = arduino('arduinoB0-1', 'arduinoB0-2', header = True)
arduino('arduinoB1-3', 'arduinoB1-4', I = 2.13, offset = C0, soffset = sC0)
arduino('arduinoB1-5', 'arduinoB1-6', I = 1.05, offset = C0, soffset = sC0)

