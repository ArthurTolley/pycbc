# Copyright (C) 2022 Arthur Tolley
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Generals
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
This module contains functions for subtracting glitches from strain data.
"""
import os
import copy
import h5py
import logging
import numpy
from typing import Union
from pycbc.types import float64, float32, TimeSeries
import pycbc.io
import scipy.signal as sig

class GlitchSubtractionSet(object):
    """Manages sets of subtractions and subtract them from time series.

    Subtractions are read from HDF files.

    Parameters
    ----------
    sim_file : string
        Path to an hdf file that contains a GlitchTable.
    \**kwds :
        The rest of the keyword arguments are passed to the artefact generation
        function when generating subtractions.

    Attributes
    ----------
    table
    """

    def __init__(self, sim_file, **kwds):
        ext = os.path.basename(sim_file)
        self._subhandler = GlitchHDFSubtractionSet(sim_file)
        self.table = self._subhandler.table
        self.apply = self._subhandler.apply
        self.make_strain_from_sub_object = \
            self._subhandler.make_strain_from_sub_object
        self.times = self._subhandler.times

    @staticmethod
    def from_cli(opt):
        """Return an instance of GlitchSubtractionSet configured as specified
        on the command line.
        """
        if opt.glitch_subtraction_file is None:
            return None

        kwa = {}
        return GlitchSubtractionSet(opt.glitch_subtraction_file, **kwa)


class GlitchHDFSubtractionSet():
    """Manages glitch subtractions.
    """
    
    _tableclass = pycbc.io.FieldArray
    sl_required_params = ('fringe_frequency', 'time_period',
                          'amplitude', 'phase', 'time_of')
    
    def __init__(self, sim_file, hdf_group=None, **kwds):
        
        # TODO: This needs to filter the hdf file by detector and provide a warning
        #  for mismatched frame and channel names.
        
        # open the file
        fp = h5py.File(sim_file, 'r')
        
        # Scattered Light specific parameters - to be generalised
        sl_parameters = ['fringe_frequency', 'time_period', 'amplitude', 'phase', 'centre_time']
        sl_dataset = fp['scattered_light']
        subvals = {param: sl[param] for param in sl_parameters}

        if len(sl_parameters) == 0:
            numsub = 1
        else:
            numsub = tuple(subvals.values())[0].size

        missing = set(self.sl_required_params) - set(subvals.keys())
        if missing:
            raise ValueError("Required parameter(s) {} not found in the given "
                             "subtraction file".format(', '.join(missing)))

        # initialize the table
        self.table = self._tableclass.from_kwargs(**subvals)

    
    def apply(self, strain, subtraction_sample_rate=None):
        """Add subtractions to a time series.

        Parameters
        ----------
        strain : TimeSeries
            Time series to subtract artefacts from, of type float32 or float64.
        subtraction_sample_rate: float, optional
            The sample rate to generate the artefact before subtraction

        Returns
        -------
        None

        Raises
        ------
        TypeError
            For invalid types of `strain`.
        """
        if strain.dtype not in (float32, float64):
            raise TypeError("Strain dtype must be float32 or float64, not " \
                    + str(strain.dtype))
            
        t0 = float(strain.start_time)
        t1 = float(strain.end_time)

        delta_t = strain.delta_t
        if subtraction_sample_rate is not None:
            delta_t = 1.0 / subtraction_sample_rate

        subtractions = self.table

        subtracted_ids = []
        for ii, sub in enumerate(subtractions):

            start_time = float(sub['time_of']) - 0.5 * float(sub['time_period']) - 1
            end_time = float(sub['time_of']) + 0.5 * float(sub['time_period']) + 1
            if end_time < t0 or start_time > t1:
                continue
            
            logging.info('Subtracting artefact at %s', float(sub['time_of']))
            
            # Create the time series object containing the artefact
            signal = self.make_strain_from_sub_object(sub, 1.0/delta_t)
            
            # Place it at the right time with the right length
            length = strain.duration * (1.0/delta_t)
            template_length = len(signal)
            ts_array = numpy.zeros(int(length))
            
            # Place the artefacts at their correct time
            artefact_time = float(sub['time_of']) - float(strain.start_time)
            artefact_start_time = artefact_time - (sub['time_period'] * 0.5)
            artefact_end_time = artefact_time + (sub['time_period'] * 0.5)
            idxstart = numpy.round(artefact_start_time * (1.0/delta_t))
            idxend = numpy.round(artefact_end_time * (1.0/delta_t))
            ts_array[int(idxstart):int(idxend)] = signal
            signal = TimeSeries(ts_array, delta_t=delta_t, epoch=strain.start_time)

            # Subtract!
            strain.data -= signal
            subtracted_ids.append(ii)

        subtracted = copy.copy(self)
        subtracted.table = subtractions[numpy.array(subtracted_ids).astype(int)]
        return subtracted

    def make_strain_from_sub_object(self, sub, subtraction_sample_rate):
        """Make a h(t) strain time-series from a subtraction object.

        Parameters
        -----------
        sub : subtraction object
            The subtraction object to turn into a strain h(t). Can be any
            object which has artefact parameters as attributes, such as an
            element in a ``FieldArray``.
        delta_t : float
            Sample rate to make subtraction at.

        Returns
        --------
        signal : float
            h(t) corresponding to the subtraction.
        """

        # Compute the scattered light artefact time series
        generator = scattered_light_generator(fringe_frequency = sub['fringe_frequency'],
                                              timeperiod = sub['time_period'],
                                              amplitude = sub['amplitude'],
                                              phase = sub['phase'],
                                              time_of_artefact = sub['time_of'],
                                              start_time = 0,
                                              data_time_length = None,
                                              sample_rate = subtraction_sample_rate,
                                              pad = False,
                                              time_shift = False,
                                              roll = False)
        
        signal = generator.generate_template()

        return signal

    def times(self):
        """Return the times of all subtractions"""
        return self.table.time_of   
    

class ScatteredLightGenerator:
    """A class containing the artefact generation methods for generating
    scattered light glitches.
    
    Scattered light glitches are generated with the centre of the arch
    half way through the time series. The 'pad' parameter will extend
    the time series to be equal in length to the 'data_time_length'.
    The 'roll' parameter will roll the artefact so the centre of the
    arch will be at time = 0.

    Inputs
    ------
    fringe_frequency : float
        The fringe frequency of the artefact to be generated.
    timeperiod : float
        The time period of the artefact to be generated.
    amplitude : float
        The amplitude of the artefact to be generated.
    phase : float
        The phase of the artefact to be generated.
    time_of_artefact : float
        The time of the artefact to be generated.
        This refers to the time of the centre of the arch for scattered
          light artefacts.
    start_time : float
        The desired start time of the artefact time series.
    data_time_length : float
        The length of the data in time.
    sample_rate : float
        The sample rate of the artefact time series.
        Typically the same as that of the data.
        Default = 2048.0
    pad : bool
        Determines whether padding is added to the artefact time series.
        Default = True
    time_shift : bool
        Determines whether the time series is shifted to the artefact time_of.
        Default = True
    roll : bool
        Determines whether the artefact is rolled so the centre of the arch
          appears at time = 0 in the time series.


    Outputs
    -------
    self objects containing the inputs.

    """
    def __init__(self,
                 fringe_frequency: float,
                 timeperiod: float,
                 amplitude: float,
                 phase: float,
                 time_of_artefact: float,
                 start_time: float,
                 data_time_length: Union[float, None],
                 sample_rate: float = 2048,
                 pad: bool = True,
                 time_shift: bool = True,
                 roll: bool = True) -> None:

        
        self.fringe_frequency = fringe_frequency
        self.timeperiod = timeperiod
        self.amplitude = amplitude
        self.phase = phase
        self.time_of_artefact = time_of_artefact
        self.start_time = start_time
        self.data_time_length = data_time_length
        self.sample_rate = sample_rate
        self.pad = pad
        self.time_shift = time_shift
        self.roll = roll

    def generate_template_array(self,
                                tukey_length: float = 0.2) -> None:
        """Generate a numpy array containing the artefact.

        Inputs
        ------
        tukey_length : float
            The tukey window input to the scipy function.

        Outputs
        -------
        self.template_array : numpy.array
            A numpy array object containing the generated artefact.

        """

        t_initial = -self.timeperiod/2.0
        t_end = self.timeperiod/2.0
        dt = 1./(self.sample_rate)
        t = numpy.arange(t_initial, t_end, dt)
        f_rep = 1./(2.*self.timeperiod)

        self.template_array = self.amplitude * numpy.sin((self.fringe_frequency/f_rep)*numpy.sin(2*numpy.pi*f_rep*t) + self.phase)
        self.template_array = self.template_array * sig.tukey(len(self.template_array), tukey_length)

    def generate_template_timeseries(self) -> TimeSeries:
        """Generate a pycbc TimeSeries from a numpy array.

        Inputs
        ------

        Outputs
        -------
        self.template_timeseries : pycbc.TimeSeries
            A TimeSeries object containing the artefact.

        """

        if self.pad is True:
            length = self.data_time_length * self.sample_rate
            template_length = len(self.template_array)

            ts_array = numpy.zeros(int(length))
            idxstart = length/2 - int(template_length/2.)
            idxend = idxstart + template_length
            ts_array[int(idxstart):int(idxend)] = self.template_array
            if self.roll is True:
                ts_array = numpy.roll(ts_array, (int(len(ts_array)/2.0)))

            self.template_timeseries = TimeSeries(ts_array,
                                                  delta_t=1./self.sample_rate,
                                                  epoch=self.start_time)

        else:
            self.template_timeseries = TimeSeries(self.template_array,
                                                  delta_t=1./self.sample_rate,
                                                  epoch=self.start_time)

    def generate_template(self) -> TimeSeries:
        """Comprehensive method for template generation

        Inputs
        ------

        Outputs
        -------
        self.template_timeseries : pycbc.TimeSeries
            A TimeSeries object containing the desired artefact.

        """

        if self.time_shift is False:
            self.generate_template_array()
            self.generate_template_timeseries()
            
        if self.time_shift is True:
            self.generate_template_array()
            self.generate_template_timeseries()
            self.shift_template_in_time()

        return self.template_timeseries

    def shift_template_in_time(self) -> None:
        """Shifting the TimeSeries to move the location of the
        artefact in time.

        Inputs
        ------

        Outputs
        -------

        """

        time_shift = self.time_of_artefact - self.start_time
        self.template_timeseries = self.template_timeseries.cyclic_time_shift(time_shift)
