import h5py
import numpy

# Change chisq to be original chisq and not reduced chisq
h1_no_inj = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/new-stat-psd-var/trigger-merges/H1_new_stat_no_injs.hdf', 'a')
l1_no_inj = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/new-stat-psd-var/trigger-merges/L1_new_stat_no_injs.hdf', 'a')

h1_with_inj = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/new-stat-psd-var/trigger-merges/H1_new_stat_with_injs.hdf', 'a')
l1_with_inj = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/new-stat-psd-var/trigger-merges/L1_new_stat_with_injs.hdf', 'a')

print(h1_no_inj['H1']['chisq'][:5])
print(l1_no_inj['L1']['chisq'][:5])
print(h1_with_inj['H1']['chisq'][:5])
print(l1_with_inj['L1']['chisq'][:5])

tmpval = h1_no_inj['H1']['chisq'][:] * (2 * h1_no_inj['H1']['chisq_dof'][:] - 2)
h1_no_inj['H1']['chisq'][:] = tmpval

tmpval = l1_no_inj['L1']['chisq'][:] * (2 * l1_no_inj['L1']['chisq_dof'][:] - 2)
l1_no_inj['L1']['chisq'][:] = tmpval

tmpval = h1_with_inj['H1']['chisq'][:] * (2 * h1_with_inj['H1']['chisq_dof'][:] - 2)
h1_with_inj['H1']['chisq'][:] = tmpval

tmpval = l1_with_inj['L1']['chisq'][:] * (2 * l1_with_inj['L1']['chisq_dof'][:] - 2)
l1_with_inj['L1']['chisq'][:] = tmpval

print(h1_no_inj['H1']['chisq'][:5])
print(l1_no_inj['L1']['chisq'][:5])
print(h1_with_inj['H1']['chisq'][:5])
print(l1_with_inj['L1']['chisq'][:5])

h1_no_inj.close()
l1_no_inj.close()
h1_with_inj.close()
l1_with_inj.close()

# h1_no_inj = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/old-stat/trigger-merges/H1_old_no_test.hdf', 'a')
# print(h1_no_inj['H1']['chisq_dof'][:])
# print(h1_no_inj['H1']['chisq'][:])

# tmpval = h1_no_inj['H1']['chisq'][:] * (2 * h1_no_inj['H1']['chisq_dof'][:] - 2)
# h1_no_inj['H1']['chisq'][:] = tmpval

# print(h1_no_inj['H1']['chisq_dof'][:])
# print(h1_no_inj['H1']['chisq'][:])

# h1_no_inj.close()

