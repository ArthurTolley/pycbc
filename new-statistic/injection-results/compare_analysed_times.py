import h5py
import numpy
import sys
from ligo import segments
from pycbc import events

from ligo.lw import table, lsctables, utils as ligolw_utils
from ligo.segments import segment, segmentlist
from pycbc.io.ligolw import LIGOLWContentHandler as h


old_stat_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/old-stat/statmap/H1L1-STATMAP_INJ_with_injs.hdf', 'r')
# fits_only_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/statmap/H1L1-STATMAP_INJ_with_injs.hdf', 'r')
fits_psd_var_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/fits-psd-var/statmap/H1L1-STATMAP_INJ_with_injs.hdf', 'r')

old_stat = {}
# fits_only = {}
fits_psd_var = {}

# Create a list of every second that was analyzed by the searches
old_seconds = []
for start, end in zip(numpy.sort(old_stat_file['segments']['H1L1']['start'][:]), numpy.sort(old_stat_file['segments']['H1L1']['end'][:])):
    list_of_seconds = numpy.arange(int(start), int(end), 1)
    for second in list_of_seconds:
        old_seconds.append(second)

# Create a list of every second that was analyzed by the searches
# fit_only_seconds = []
# for start, end in zip(numpy.sort(fits_only_file['segments']['H1L1']['start'][:]), numpy.sort(fits_only_file['segments']['H1L1']['end'][:])):
#     list_of_seconds = numpy.arange(int(start), int(end), 1)
#     for second in list_of_seconds:
#         fit_only_seconds.append(second)

# Same as fit only so don't bother
fit_psd_var_seconds = []
for start, end in zip(numpy.sort(fits_psd_var_file['segments']['H1L1']['start'][:]), numpy.sort(fits_psd_var_file['segments']['H1L1']['end'][:])):
    list_of_seconds = numpy.arange(int(start), int(end), 1)
    for second in list_of_seconds:
        fit_psd_var_seconds.append(second)

print('---')
print('Time analysed by old-stat search:', len(old_seconds))
print('Time analysed by fit-psd-var search:', len(fit_psd_var_seconds))
print('Time difference (old - fit-psd-var):', len(old_seconds) - len(fit_psd_var_seconds))

# Find the values in old_seconds that are not in fit_only_seconds
values_not_in_fit_only = [i for i in (set(old_seconds) - set(fit_psd_var_seconds))]
values_not_in_old = [j for j in (set(fit_psd_var_seconds) - set(old_seconds))]

print('Time analysed by old-stat and not fit-psd-var:', len(values_not_in_fit_only))
print('Time analysed by fit-psd-var and not old-stat:', len(values_not_in_old))

# ---------------------------------------------
# any_seg.coalesce() # this is slow
# any_seg & any_seg2 # Union
# any_seg - any_seg2 # a but not b

print("---")

old_stat_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/old-stat/statmap/H1L1-STATMAP_INJ_with_injs.hdf', 'r')
fits_psd_var_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/fits-psd-var/statmap/H1L1-STATMAP_INJ_with_injs.hdf', 'r')

old_any_seg = segments.segmentlist([])
old_starts = old_stat_file['segments']['H1L1']['start'][:]
old_ends = old_stat_file['segments']['H1L1']['end'][:]
old_any_seg += events.start_end_to_segments(old_starts, old_ends)
old_ana_start, old_ana_end = events.segments_to_start_end(old_any_seg)

fits_only_any_seg = segments.segmentlist([])
fits_only_starts = fits_psd_var_file['segments']['H1L1']['start'][:]
fits_only_ends = fits_psd_var_file['segments']['H1L1']['end'][:]
fits_only_any_seg += events.start_end_to_segments(fits_only_starts, fits_only_ends)
fits_only_ana_start, fits_only_ana_end = events.segments_to_start_end(fits_only_any_seg)

old_stat_coal = old_any_seg.coalesce()
fits_only_coal = fits_only_any_seg.coalesce()

print(len(old_stat_coal), len(fits_only_coal))

print("")

union = fits_only_coal & old_stat_coal
segment_starts = [segment[0] for segment in union]
segment_ends = [segment[1] for segment in union]

all_jointly_analysed_seconds = []

for start, end in zip(segment_starts, segment_ends):
    list_of_seconds = numpy.arange(int(start), int(end), 1)
    for second in list_of_seconds:
        all_jointly_analysed_seconds.append(second)

print('Time analysed by both old-stat and fit-psd-var:', len(all_jointly_analysed_seconds))

numpy.savetxt('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint_analysed_seconds.txt',
              all_jointly_analysed_seconds,
              delimiter=',',
              fmt='%s')