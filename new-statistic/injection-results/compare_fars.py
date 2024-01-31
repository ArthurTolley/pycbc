import h5py
import numpy
def count_injections_with_ifar(ifars : list):
    ifar_limits = [0.1, 1, 10, 100]

    for lim in ifar_limits:
        print(f'Injections with ifar greater than {lim}: ', len(ifars[ifars>lim]))

old_stat_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-old-stat/hdfinjfind/H1L1-HDFINJFIND_BBH_RATESINJ_INJECTIONS-1262995020-600000.hdf', 'r')
fits_psd_var_file = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-fits-psd-var/hdfinjfind/H1L1-HDFINJFIND_BBH_RATESINJ_INJECTIONS-1262995020-600000.hdf', 'r')

old_stat = {}
fits_psd_var = {}

old_stat['template_id'] = old_stat_file['found']['template_id'][:]
old_stat['ifar_exc'] = old_stat_file['found']['ifar_exc'][:]
old_stat['injection_index'] = old_stat_file['found']['injection_index'][:]

fits_psd_var['template_id'] = fits_psd_var_file['found']['template_id'][:]
fits_psd_var['ifar_exc'] = fits_psd_var_file['found']['ifar_exc'][:]
fits_psd_var['injection_index'] = fits_psd_var_file['found']['injection_index'][:]

print(f'Old Stat: Number of injections found: {len(old_stat["ifar_exc"])}')
print('-----------------------------------')
count_injections_with_ifar(old_stat['ifar_exc'])
print('')
print(f'Fits & PSD Var: Number of injections found: {len(fits_psd_var["ifar_exc"])}')
print('-----------------------------------')
count_injections_with_ifar(fits_psd_var['ifar_exc'])

old_stat_file.close()
fits_psd_var_file.close()