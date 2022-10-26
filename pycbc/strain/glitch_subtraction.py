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
import logging
import numpy
from typing import Union
from pycbc.filter import make_frequency_series
from pycbc.types import TimeSeries, FrequencySeries, zeros
import scipy.signal as sig

class scattered_light:
    """A class containing the artefact generation methods for generating
    scattered light.
    
    Scattered light artefacts are generated with the centre of the arch
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

    # Scattered Light Model

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

        if self.time_shift = False:
            self.generate_template_array()
            self.generate_template_timeseries()
            
        if self.time_shift = True:
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
        
        