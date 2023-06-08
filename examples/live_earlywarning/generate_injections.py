#!/usr/bin/env python

import sys
import numpy as np
from pycbc.io import FieldArray
from pycbc.inject import InjectionSet


dtype = [('mass1', float), ('mass2', float),
         ('spin1z', float), ('spin2z', float),
         ('tc', float), ('distance', float),
         ('ra', float), ('dec', float),
         ('approximant', 'S32')]

static_params = {'f_lower': 18.,
                 'f_ref': 18.,
                 'taper': 'start',
                 'inclination': 0.,
                 'coa_phase': 0.,
                 'polarization': 0.}

# 1 injection
samples = FieldArray(1, dtype=dtype)

# 
samples['mass1'] = [1.5]
samples['mass2'] = [1.5]
samples['spin1z'] = [0.]
samples['spin2z'] = [0.]

# 
samples['tc'] = [1365890089.9]
samples['distance'] = [14.]
samples['ra'] = [np.deg2rad(45)]
samples['dec'] = [np.deg2rad(45)]

samples['approximant'] = ['SpinTaylorT4']

InjectionSet.write('injections.hdf', samples, static_args=static_params,
                   injtype='cbc', cmd=" ".join(sys.argv))
