import h5py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.colors import SymLogNorm
import numpy as np

fits = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/vt_calculation/fits_coinc_combined_filtered.hdf'
old = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/vt_calculation/old_coinc_combined_filtered.hdf'

fits_combined_file = h5py.File(fits, 'r')
old_combined_file = h5py.File(old, 'r')

fits_combined_df = pd.DataFrame(columns=fits_combined_file.keys())
for key in fits_combined_df.keys():
    fits_combined_df[key] = fits_combined_file[key][:]

old_combined_df = pd.DataFrame(columns=old_combined_file.keys())
for key in old_combined_df.keys():
    old_combined_df[key] = old_combined_file[key][:]

# --------------------------------------------------------
all_kept_keys = ['H1_chisq', 'H1_end_time', 'H1_psd_var_val', 'H1_sg_chisq',
                 'H1_sigmasq', 'H1_snr', 'L1_chisq', 'L1_end_time',
                 'L1_psd_var_val', 'L1_sg_chisq', 'L1_sigmasq', 'L1_snr',
                 'chirp_mass', 'ifar_exclusive', 'injection_index', 'mass1',
                 'mass2', 'network_snr', 'p_value_exclusive', 'spin1z',
                 'spin2z', 'stat', 'time']

cut_keys = ['H1_chisq', 'H1_psd_var_val', 'H1_sg_chisq', 'H1_sigmasq',
             'H1_snr', 'L1_chisq', 'L1_psd_var_val', 'L1_sg_chisq',
             'L1_sigmasq', 'L1_snr', 'ifar_exclusive', 'injection_index',
             'network_snr', 'stat']

# Cut all injections not find with an old_stat IFAR > 1.0
#  Allows us to find a subsection of injections that have dropped IFAR
inj_idxs_filter = old_combined_df['injection_index'][old_combined_df['ifar_exclusive'] > 1.0]
fits_combined_df = fits_combined_df[fits_combined_df['injection_index'].isin(inj_idxs_filter)]
old_combined_df = old_combined_df[old_combined_df['injection_index'].isin(inj_idxs_filter)]

# print(fits_combined_df.loc[fits_combined_df['injection_index'] == 10583.0][all_kept_keys].T)
# print(old_combined_df.loc[old_combined_df['injection_index'] == 10583.0][all_kept_keys].T)

kept_keys = ['injection_index', 'H1_snr', 'L1_snr', 'network_snr', 'stat',
             'ifar_exclusive', ]

fits_combined_df = fits_combined_df[all_kept_keys]#.loc[fits_combined_df['ifar_exclusive'] > 0.1]
old_combined_df = old_combined_df[all_kept_keys]#.loc[old_combined_df['ifar_exclusive'] > 0.1]

joined_df = pd.merge(fits_combined_df, old_combined_df, on='injection_index', suffixes=('_F', '_O'))
joined_df['ifar_diff']  = joined_df['ifar_exclusive_F'] - joined_df['ifar_exclusive_O']
joined_df['ifar_frac_diff'] = ((joined_df['ifar_exclusive_F'] - joined_df['ifar_exclusive_O']) / joined_df['ifar_exclusive_O'])
print('Jointly observed injections', len(joined_df))
# print(joined_df)
# print(joined_df['ifar_diff'])

better_ifar = ((joined_df['ifar_exclusive_F'] - joined_df['ifar_exclusive_O']) / joined_df['ifar_exclusive_O']) > 0.0
worse_ifar = ((joined_df['ifar_exclusive_F'] - joined_df['ifar_exclusive_O']) / joined_df['ifar_exclusive_O']) < -0.01
print("Num Better: ", sum(better_ifar))
print("Num Worse: ", sum(worse_ifar))

joined_better_df = joined_df[better_ifar]
joined_worse_df = joined_df[worse_ifar]

joined_worse_df = joined_worse_df.sort_values(by='ifar_diff', ascending=True)
joined_better_df = joined_better_df.sort_values(by='ifar_diff', ascending=False)

joined_worse_df.sort_values(by='ifar_frac_diff', ascending=True).to_csv('worse_ifar_frac.csv')

print(joined_df.sort_values(by='ifar_frac_diff', ascending=False))

# IFAR vs IFAR
if True:
    fig = plt.figure(figsize=(9, 7))
    plt.xlabel('Old Stat')
    plt.ylabel('Fits & PSD Var')
    plt.plot([1e-5, 1e5], [1e-5, 1e5], linestyle=':', color='k')
    plt.vlines(1, 1e-5, 1e5, linestyle='--', color='r', alpha=0.5)
    plt.hlines(1, 1e-5, 1e5, linestyle='--', color='r', alpha=0.5)
    plt.xlim(1e-5, 1e5)
    plt.ylim(1e-5, 1e5)
    scatter = plt.scatter(joined_df['ifar_exclusive_O'], joined_df['ifar_exclusive_F'],
                          c=joined_df['ifar_diff'], cmap='cividis', marker='x', s=5, norm=SymLogNorm(linthresh=1))
    plt.colorbar(scatter, label='ifar_diff', format='%.0e')  # Set format to scientific notation
    plt.loglog()
    plt.savefig('fits_vs_old_colour_filtered.png')
    plt.close()

    # fig = plt.figure(figsize=(9, 7))
    # plt.xlabel('Old Stat')
    # plt.ylabel('Fits & PSD Var')
    # plt.plot([1e-5, 1e5], [1e-5, 1e5], linestyle=':', color='k')
    # plt.vlines(1, 1e-5, 1e5, linestyle='--', color='r', alpha=0.5)
    # plt.hlines(1, 1e-5, 1e5, linestyle='--', color='r', alpha=0.5)
    # plt.xlim(1e-5, 1e5)
    # plt.ylim(1e-5, 1e5)
    # scatter = plt.scatter(joined_df['ifar_exclusive_O'], joined_df['ifar_exclusive_F'],
    #                       c=joined_df['ifar_frac_diff'], cmap='cividis', marker='x', s=5, norm=SymLogNorm(linthresh=1))
    # plt.colorbar(scatter, label='ifar_diff', format='%.0e')  # Set format to scientific notation
    # plt.loglog()
    # plt.savefig('fits_vs_old_colour_frac.png')
    # plt.close()



# --------------------------------------------------------
fits_combined_file.close()
old_combined_file.close()
