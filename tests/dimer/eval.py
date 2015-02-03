#! /usr/bin/env python

from StringIO import StringIO

import numpy as np

import ase.io as io

###

f = open('OUT')
l = f.readline()
while l.split()[0] != 'Step':
    l = f.readline()
s = StringIO()
l = f.readline()
while l.split()[0] != 'Loop':
    s.write(l)
    l = f.readline()
step, ect, ecoul, etot = np.loadtxt(StringIO(s.getvalue()), usecols=[0, 4, 6, 3], unpack=True)
step = np.array(step, dtype=int)
dist = np.array([io.read('dump.custom', index=i).get_distance(0, 1) for i in step])
charges1 = np.array([io.read('dump.custom', index=i).get_array('charges')[0] for i in step])
charges2 = np.array([io.read('dump.custom', index=i).get_array('charges')[1] for i in step])

###

# Charges should have equal magnitude but opposite sign

assert np.all(np.abs(charges1+charges2) < 1e-9)

###

X = 1.0
U = 0.1
V = 0.1
p = 2

# Check Coulomb energy

ecoul_check = charges1*charges2/dist

assert np.all(np.abs(ecoul-ecoul_check) < 1e-3)

# Check energy from charge-transfer model

ect_check  = X*(charges1-charges2)
ect_check += 0.5*U*charges1**2 + 0.5*U*charges2**2
ect_check += 0.5*V*charges1**p + 0.5*V*charges2**p

assert np.all(np.abs(ect-ect_check) < 1e-3)

# Check charges
# Total energy:    -q**2/dist + 2*X*q + (U+V)*q**2
# Derivative:      -2*q/dist + 2*X + 2*(U+V)*q
# Equilibrium at:  q = X/(1.0/dist-U-V)

charges_check = X/(1.0/dist-U-V)

assert np.all(np.abs(charges1-charges_check))