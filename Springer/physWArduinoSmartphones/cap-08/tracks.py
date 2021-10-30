import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.optimize import curve_fit
# load and show an image with Pillow
from PIL import Image
#
# open the image form working directory
# first of all make a qualitative analysis on a portion of the image
#
image = Image.open('tracksmall.jpg')
# summarize some details about the image
print(image.format)
print(image.size)
print(image.mode)
# transform the imnage into a list
data = np.asarray(image)
lx = len(data) - 1;
ly = len(data[0]) - 1
lz = len(data[0][0]) - 1
print(lx)
print(ly)
print(lz)
# dump the image using colored ASCII characters
for row in data:
    for pixel in row:
        h = int(pixel[0]) + int(pixel[1]) + int(pixel[2])
        ch = ''
        if h > 32:
            ch = '\033[0;' + str(30 + h % 7) + 'm'
        print(ch + 'O\033[0m', end='')
    print()
# open the full image
image = Image.open('tracks.jpg')
data = np.asarray(image)
# a NxM image is a list of N lists, each with M elements
lx = len(data);
ly = len(data[0]);
print('Format: {} x {}'.format(lx, ly))

c = []
p = []
i = 0
k = 0
N = lx / 10
M = ly / 15
N2 = N * M
threshold = 600
# iterate over the rows in the list
for row in data:
    # iterate over the pixels in the row
    for pixel in row:
        i += 1
        # sum the fired pixels every NxM
        if (i % N2) == 0:
            c.append(k)
            k = 0
        # every pixel is in fact a list of three numbers
        h = int(pixel[0]) + int(pixel[1]) + int(pixel[2])
        p.append(h)
        if h > threshold:
            k += 1

def fexp(x, A, b):
    return A*np.exp(-x/b)

bins = np.arange(0, 766, 10)

# make a histogram of the intensity of the pixels in log scale
plt.figure(figsize=(8.5,4))
ch, bins, patch = plt.hist(p, bins)
print(bins)
plt.yscale('log')
plt.xlabel('pixel intensity')
plt.savefig('tracks-histo.png')
plt.show()

pexp, cov = curve_fit(fexp, bins[16:22], ch[16:22], p0 = (22000, 8.5))
print(pexp)

# remake the histogram with a linear scale, showing only part of the yscale
plt.figure(figsize=(8.5,4))
plt.hist(p, bins)
plt.plot(bins, fexp(bins, pexp[0], pexp[1]), '-')
plt.ylim(0, 1250)
plt.xlabel('pixel intensity')
plt.savefig('tracks-histo-zoomed.png')
plt.yscale('linear')
plt.show()

plt.figure(figsize=(8.5,4))
for i in range(len(ch)):
    ch[i] -= fexp(bins[i], pexp[0], pexp[1])
plt.plot(bins[:-1], ch, 'o')
plt.ylim(0, 1250)
plt.title('Noise subtracted histogram')
plt.xlabel('pixel intensity')
plt.show()

# compute statistics
avg = np.average(c)
rms = np.std(c)
print('Average = {}'.format(avg))
print('RMS = {}'.format(rms))

mu = (avg/rms)**2
print('Mean = {}'.format(mu))
cal = avg/mu
print('Calibration = {}'.format(cal))

# make a histogram of the high energy hits
plt.figure(figsize=(8.5,4))
ch, bins, patch = plt.hist(c, bins = np.arange(0, cal*mu*4, cal * 2))
binwidth = bins[1] - bins[0]
S = sum(ch)
    
print('Integral = {}'.format(S))
print('bin width = {}'.format(binwidth));

# make a plot of the data together with the Poisson distribution 
xx = range(int(math.ceil(mu*4)))
yy = poisson.pmf(xx, mu)
print(xx)
print(yy)
plt.plot(xx*cal, S*yy*binwidth/cal, '-')
plt.xlabel('pixel counts')
plt.savefig('tracks-poisson.png')
plt.show()
