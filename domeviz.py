# Built-in
import getopt
import math
import socket
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

# Socket constants
SOCK_IP = "192.168.10.5"
SOCK_START_PORT = 19850
SOCK_MAX_LEDS = 484

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

# Create map between numbering vertices from middle, and 
# how it's numbered in pyDome
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

# And create the LEDs
led_list = []
for c in C_new:
    start = vpython.vector(*V[new_v[c[0]]])
    end = vpython.vector(*V[new_v[c[1]]])
    if (end - start).mag < 0.01:
        # Dud cord
        print("Ignoring {}".format(c))
        continue

    direc = ((end - start) * sep) / (end - start).mag
    length = round((end - start).mag,2)
    if length == 0.71:
        leds = 35
    if length == 0.83:
        leds = 41
    if length == 0.82:
        leds = 41
    if length == 0.88:
        leds = 44
    if length == 0.91:
        leds = 46
    if length == 0.84:
        leds = 42

    for i in range(leds):
        led = vpython.sphere(pos = start + (direc * (i + 4)), radius = 0.003)
        led_list.append(led)

# Create the listening ports
sock_ports = []
for i in range(math.ceil(len(led_list)/SOCK_MAX_LEDS)):
    port = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port.setblocking(False)
    port.bind((SOCK_IP, SOCK_START_PORT + i))

    sock_ports.append(port)

# Do shit with LEDs
while True:
    for port_idx, port in enumerate(sock_ports):
        try:
            data, addr = port.recvfrom(SOCK_MAX_LEDS*3+43)
        except BlockingIOError:
            # No UDP packet
            continue
        for i in range(SOCK_MAX_LEDS):
            
            try:
                r = int(data[i*3])
                g = int(data[(i*3)+1])
                b = int(data[(i*3)+2])
            except IndexError:
                # End of data
                pass
            led_list[i + (port_idx * SOCK_MAX_LEDS)].color = vpython.vector(r, g, b)
