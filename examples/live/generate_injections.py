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

static_params = {'f_lower': 17.,
                 'f_ref': 17.,
                 'taper': 'start',
                 'inclination': 0.,
                 'coa_phase': 0.,
                 'polarization': 0.}

samples = FieldArray(1, dtype=dtype)

# masses and spins are intended to match the highest
# and lowest mass templates in the template bank
# Last injection is designed to be found as an EM-bright single
samples['mass1'] = [2.9756491]
samples['mass2'] = [1.1077247]
samples['spin1z'] = [0.39105825]
samples['spin2z'] = [0.047548451]

# distance and sky locations for coincs to have network SNRs ~15
# and for single to pass SNR cuts
samples['tc'] = [1272790100.3]
samples['distance'] = [47.]
samples['ra'] = [np.deg2rad(10)]
samples['dec'] = [np.deg2rad(-45)]

samples['approximant'] = ['SpinTaylorT4']

InjectionSet.write('injections.hdf', samples, static_args=static_params,
                   injtype='cbc', cmd=" ".join(sys.argv))
