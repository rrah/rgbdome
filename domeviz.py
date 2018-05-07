# Built-in
import getopt
import math
import sys
import time

# PIP
import numpy
import vpython

# pyDome
import pyDome.Polyhedral
import pyDome.SymmetryTriangle
import pyDome.GeodesicSphere
import pyDome.Output
import pyDome.Truncation

# Constants for leds
sep = 1/60

# Set up vpython view
screen = vpython.canvas(width = 1900, height = 992)

# Constants for pyDome
radius = numpy.float64(2.8)
frequency = 4
polyhedral = pyDome.Polyhedral.Icosahedron()
vertex_equal_threshold = 0.0000001
truncation_amount = 0.499999

# Create the dome info
symmetry_triangle = pyDome.SymmetryTriangle.ClassOneMethodOneSymmetryTriangle(frequency, polyhedral)
sphere = pyDome.GeodesicSphere.GeodesicSphere(polyhedral, symmetry_triangle, vertex_equal_threshold, radius)

V, C = pyDome.Truncation.truncate(sphere.sphere_vertices, sphere.non_duplicate_chords, truncation_amount)

v_sort = []
for i, v in enumerate(V):
    x = v[0]
    y = v[1]

    r = ((x ** 2) + (y ** 2)) ** 0.5
    if y == 0:
        t = 180 if x < 0 else 0
    elif x == 0:
        t = 90 if y > 0 else 270
    else:
        t = numpy.arctan2(y, x)
        if t < 0:
            t += 2*numpy.pi
    v_sort.append((r, t, i)) 

v_sort.sort(key = lambda x: (round(x[0], 5), round(x[1], 8)))
new_v = [x[2] for x in v_sort]

C_new = []

for c in C:
    x = c[0] - 1
    y = c[1] - 1
    x_n = new_v.index(x)
    y_n = new_v.index(y)

    if x_n < y_n:
        C_new.append((x_n, y_n))
    else:
        C_new.append((y_n, x_n))

C_new.sort(key = lambda x: (x[0], x[1]))

print(C_new)

# And create the LEDs
led_list = []
for c in C_new:
    start = vpython.vector(*V[new_v[c[0]]])
    end = vpython.vector(*V[new_v[c[1]]])
    if (end - start).mag < 0.01:
        # Dud cord
        continue

    direc = ((end - start) * sep) / (end - start).mag
    length = round((end - start).mag,2)
    if length == 0.71:
        leds = 35
    if length == 0.83:
        leds = 41
    if length == 0.82:
        leds = 42
    if length == 0.88:
        leds = 44
    if length == 0.91:
        leds = 46
    if length == 0.84:
        leds = 42

    for i in range(leds):
        led = vpython.sphere(pos = start + (direc * (i + 4)), radius = 0.003)
        led_list.append(led)

# Do shit with LEDs
while True:
    for color in [vpython.vector(1,0,0), vpython.vector(0,1,0), vpython.vector(0,0,1)]:
        for led in led_list:
            led.color = color
            time.sleep(0.01)