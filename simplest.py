import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import accumulate

data = pd.read_csv('Raw Data.csv')
print(data)

ax = data['Acceleration x (m/s^2)']
ay = data['Acceleration y (m/s^2)']
az = data['Acceleration z (m/s^2)']
tt = data['Time (s)']

#plt.plot(tt, ay)
#plt.title('Individua il tempo minimo e massimo da considerare')
#plt.show()

tmin = float(input('Inserisci t_min: '))
tmax = float(input('Inserisci t_max: '))
t = [t for t in tt if t > tmin and t < tmax]
ay = [ay for t, ay in zip(tt, ay) if t > tmin and t < tmax]

plt.plot(t, ay)
plt.show()

t0 = t[0]
t = [t - t0 for t in t]

a0 = np.mean(ay[:30])
a0 = ay[0]
ay = [ay - a0 for ay in ay]

dt = np.mean([t1-t0 for t0, t1 in zip(t[:-1], t[1:])])

print(dt)

vy = [0]
for a in ay:
    vy.append(vy[-1] + a*10*dt)

yy = [0]
for v in vy: 
    yy.append(yy[-1] + v*10*dt)
    
plt.plot(t, ay, label = 'a [m/s$^2$]')
plt.plot(t, vy[:-1], label = 'v [cm/s]')
plt.plot(t, yy[:-2], label = 'y [mm]')
plt.legend()
plt.xlabel('t [s]')
plt.ylabel('a [m/s$^2$], v [cm/s], y [mm]')
plt.show()



        

