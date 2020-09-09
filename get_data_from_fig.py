from __future__ import print_function
from __future__ import division

import json
import math

import numpy as np
import matplotlib.pylab as plt
from PIL import Image


im = Image.open('Co-II-Oh.jpg')
im = np.array(im)



height, width, _ = im.shape


# find data dots
r = 2
r2 = r*r
dots = []
for i in range(height):
    for j in range(width):

        if im[i, j, 2] >= 200 and im[i, j, 0] <=50 and im[i, j, 1] <=50:
            is_data = True
            for ni in range( max(0, int(i-r)), min(height, int(i+r)) ):
                for nj in range( max(0, int(j-r)), min(width, int(j+r)) ):
                    if (ni-i)**2+(nj-j)**2 <= r2:
                        if im[ni, nj, 2] <= 200 or im[ni, nj, 0] >= 100 or im[ni, nj, 1] >= 100:
                            is_data = False

            if is_data:
                im[i, j] = [255, 255, 0]
                dots.append( np.array([i, j]) )


data = []
while True:
    dot0 = dots[0]
    
    _dots = []
    center = dot0
    for idx, dot in enumerate(dots[1:]):
        if np.linalg.norm(dot0-dot) <= r*1.5:
            center = center + dot
        else:
            _dots.append(dot)
    data.append( center/(len(dots)-len(_dots)) )
    dots = _dots
    
    if len(dots) == 0:
        break



# find boundry dots
dots = []
for i in range(height):
    for j in range(width):

        if im[i, j, 0] >= 200 and im[i, j, 1] <=50 and im[i, j, 2] <=50:
            is_data = True
            for ni in range( max(0, int(i-r)), min(height, int(i+r)) ):
                for nj in range( max(0, int(j-r)), min(width, int(j+r)) ):
                    if (ni-i)**2+(nj-j)**2 <= r2:
                        if im[ni, nj, 0] <= 200 or im[ni, nj, 1] >= 100 or im[ni, nj, 2] >= 100:
                            is_data = False

            if is_data:
                im[i, j] = [255, 255, 0]
                dots.append( np.array([i, j]) )

Image.fromarray(im).show()

_boundries = []
while True:
    dot0 = dots[0]
    
    _dots = []
    center = dot0
    for idx, dot in enumerate(dots[1:]):
        if np.linalg.norm(dot0-dot) <= r*1.5:
            center = center + dot
        else:
            _dots.append(dot)
    _boundries.append( center/(len(dots)-len(_dots)) )
    dots = _dots
    
    if len(dots) == 0:
        break

boundries = [None, None, None, None]
boundries[0] = np.min([i[0] for i in _boundries])
boundries[1] = np.max([i[0] for i in _boundries])
boundries[2] = np.min([i[1] for i in _boundries])
boundries[3] = np.max([i[1] for i in _boundries])

values = [1.3, 0, 775, 785]

for d in data:
    d[0] = (values[0]-values[1])/(boundries[0]-boundries[1]) * ((d[0])-boundries[0]) + values[0]
    d[1] = (values[2]-values[3])/(boundries[2]-boundries[3]) * ((d[1])-boundries[2]) + values[2]
    d[0], d[1] = d[1], d[0]



data = sorted(data, key=lambda x:x[0])
data = np.array(data)
plt.plot(data[:, 0], data[:, 1], '-o')
plt.show()


with open('Co-II-Oh.txt', 'w') as f:
    for d in data:
        f.write('%20.10f %20.10f \n'%(d[0], d[1]))
