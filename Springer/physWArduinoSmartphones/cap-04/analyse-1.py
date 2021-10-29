import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) <= 1:
    print('Usage: analyse.py [filename]')
else:
    filename = sys.argv[1]
    unit = 'a.u.'
    if len(sys.argv) > 2:
        unit = sys.argv[2]
    f = pd.read_csv(filename)
    data = f.T.values.tolist()
    h, bins, rect = plt.hist(x=data[1], bins='auto')
    print('============ histogram content ===============')
    print(h)
    print('==============================================')
    plt.xlabel('Illuminance [{}]'.format(unit))
    mean = np.mean(data[1])
    median = np.median(data[1])
    stdev = np.std(data[1])
    print('Average = ' + str(mean))
    print('Average = ' + str(median))
    print('StDev   = ' + str(stdev))
    plt.show()
