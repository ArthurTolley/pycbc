import glob
import numpy
import h5py
import sys

old_stat_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/old-stat/statmap/H1L1-STATMAP_INJ_with_injs.hdf', 'r')
fits_psd_var_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-psd-var/statmap/H1L1-STATMAP_INJ_with_injs.hdf', 'r')

old_stat = {}
fits_psd_var = {}

# Create a list of every second that was analyzed by the searches
old_seconds = []
for start, end in zip(numpy.sort(old_stat_file['segments']['H1L1']['start'][:]), numpy.sort(old_stat_file['segments']['H1L1']['end'][:])):
    list_of_seconds = numpy.arange(int(start), int(end), 1)
    for second in list_of_seconds:
        old_seconds.append(second)

# Same as fit only so don't bother
fit_psd_var_seconds = []
for start, end in zip(numpy.sort(fits_psd_var_file['segments']['H1L1']['start'][:]), numpy.sort(fits_psd_var_file['segments']['H1L1']['end'][:])):
    list_of_seconds = numpy.arange(int(start), int(end), 1)
    for second in list_of_seconds:
        fit_psd_var_seconds.append(second)

values_in_both = [i for i in (set(old_seconds) & set(fit_psd_var_seconds))]
print(len(values_in_both))
values_in_both = [val for val in values_in_both if val % 4 == 0]
print(len(values_in_both))

week1_start=1262390400
week1_end=1262995200

week2_start=1262995020
week2_end=1263600000

# To prevent end of week 1 injections from being seen, re-position week 2 start
week2_start=1262995020 + 180
week2_end=1263600000

values_in_both = set([val for val in values_in_both if val > week2_start and val < week2_end])
print(len(values_in_both))

no_injs = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_no_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:20]) in values_in_both
]

with_injs = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_with_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:20]) in values_in_both
]
print(len(no_injs))
print(len(with_injs))

# numpy.savetxt('JOINT_old_stat_no_injs.txt', no_injs, delimiter=',', fmt='%s')
# numpy.savetxt('JOINT_old_stat_with_injs.txt', with_injs, delimiter=',', fmt='%s')

no_injs = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/week-2/new-stat/no-injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:20]) in values_in_both
]

with_injs = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/week-2/new-stat/with-injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:20]) in values_in_both
]
print(len(no_injs))
print(len(with_injs))

# numpy.savetxt('JOINT_new_stat_no_injs.txt', no_injs, delimiter=',', fmt='%s')
# numpy.savetxt('JOINT_new_stat_with_injs.txt', with_injs, delimiter=',', fmt='%s')

