import glob
import numpy as np

week2_start = 1262995020
week2_end = 1263600000

old_stat = [
    float(l.split('/')[-1][10:27]) for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_with_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week2_start and float(l.split('/')[-1][10:27]) < week2_end
]

new_stat = [
    float(l.split('/')[-1][10:27]) for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/week-2/new-stat/with-injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week2_start and float(l.split('/')[-1][10:27]) < week2_end
]

old_stat_array = np.array(old_stat)
new_stat_array = np.array(new_stat)

# Find elements in old_array but not in new_array
elements_in_old_not_in_new = np.setdiff1d(old_stat_array, new_stat_array)

# Find elements in new_array but not in old_array
elements_in_new_not_in_old = np.setdiff1d(new_stat_array, old_stat_array)

print("Elements in old_array but not in new_array:", elements_in_old_not_in_new)
print("Elements in new_array but not in old_array:", elements_in_new_not_in_old)

print(str(elements_in_new_not_in_old[1]))
print(str(elements_in_old_not_in_new[2]))








