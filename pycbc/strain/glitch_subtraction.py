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

import scipy.signal as sig

import pycbc.strain
from pycbc.events.coinc import cluster_over_time
from pycbc.filter import highpass, matched_filter, matched_filter_core, sigma, \
                         resample_to_delta_t, sigmasq, make_frequency_series
from pycbc.frame import query_and_read_frame, read_frame
from pycbc.psd import interpolate, inverse_spectrum_truncation
from pycbc.fft import IFFT
from pycbc.types.timeseries import TimeSeries, FrequencySeries, zeros
from pycbc.types import complex_same_precision_as
from ligotimegps import LIGOTimeGPS
from pycbc.filter.matchedfilter import _BaseCorrelator

class ArtefactGeneration:
    """A class containing the artefact generation methods.

    Inputs
    ------
    start_time : float
        The desired start time of the artefact time series.
    data_time_length : float
        The length of the data in time.
    fringe_frequency : float
        The fringe frequency of the artefact to be generated.
    timeperiod : float
        The time period of the artefact to be generated.
    amplitude : float
        The amplitude of the artefact to be generated
    phase : float
        The phase of the artefact to be generated
    pad : bool
        Determines whether padding is added to the artefact time series.
        Default = True
    sample_rate : float
        The sample rate of the artefact time series.
        Typically the same as that of the data.
        Default = 2048.0
    psd : pycbc.FrequencySeries
        The power spectral density to weight the template by when
        performing the whitening.
        If no whitening is needed, doesn't need to be provided.
        Default = None

    Outputs
    -------
    self objects containing the inputs.

    """
    def __init__(self,
                 start_time: float,
                 data_time_length: Union[float, None],
                 fringe_frequency: float,
                 timeperiod: float,
                 amplitude: float,
                 phase: float,
                 pad: bool = True,
                 sample_rate: float = 2048,
                 psd: FrequencySeries = None,
                 roll: bool = True) -> None:

        self.start_time = start_time
        self.data_time_length = data_time_length
        self.fringe_frequency = fringe_frequency
        self.timeperiod = timeperiod
        self.amplitude = amplitude
        self.phase = phase
        self.pad = pad
        self.sample_rate = sample_rate
        self.psd = psd
        self.roll = roll

        self.fs_temp = None

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

        self.generate_template_array()
        self.generate_template_timeseries()

        return self.template_timeseries

    def generate_frequency_template(self) -> FrequencySeries:

        self.fs_temp = make_frequency_series(self.template_timeseries)

        return self.fs_temp

    def whiten_template(self,
                        psd: FrequencySeries) -> TimeSeries:
        """Whiten the template using a provided psd.

        Inputs
        ------
        psd : pycbc.FrequencySeries
            The power spectral density to whiten the template.

        Outputs
        -------
        white_template : pycbc.TimeSeries
            A TimeSeries containing the whitened template.

        """

        if self.psd is None:
            logging.info('Please provide a psd to whiten a template.')

        white_template = (self.fs_temp / psd**0.5).to_timeseries()

        return white_template