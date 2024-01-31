import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fits_combined = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/vt_calculation/fits_coinc_combined.hdf'
old_combined = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/vt_calculation/old_coinc_combined.hdf'
inj_file_path = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/injection-frames/bbh_injs-1262192988-1263751886.hdf'

fits_combined_file = h5py.File(fits_combined, 'r')
old_combined_file = h5py.File(old_combined, 'r')
inj_file = h5py.File(inj_file_path, 'r')

fits_combined_df = pd.DataFrame(columns=fits_combined_file.keys())
for key in fits_combined_df.keys():
    fits_combined_df[key] = fits_combined_file[key][:]

old_combined_df = pd.DataFrame(columns=old_combined_file.keys())
for key in old_combined_df.keys():
    old_combined_df[key] = old_combined_file[key][:]

inj_file_df = pd.DataFrame(columns=inj_file.keys())
for key in inj_file_df.keys():
    inj_file_df[key] = inj_file[key][:]
inj_file_df = inj_file_df.sort_values(by='tc')
inj_file_df = inj_file_df.reset_index(drop=False)
inj_file_df = inj_file_df.rename(columns={'index': 'injection_index'})
inj_time_df = inj_file_df.loc[:, ['injection_index', 'tc']]

# --------------------------------------------------------
fits_combined_df = fits_combined_df.sort_values(by='time')
fits_filter = []
injs = []
for time in set(fits_combined_file['time']):
    for inj in set(inj_file_df['tc'][:]):
        if time > inj - 0.5 and time < inj + 0.5:
            fits_filter.append(time)
            injs.append(inj)
            break

fits_combined_df = fits_combined_df[fits_combined_df['time'].isin(fits_filter)].reset_index(drop=True)
inj_time_df = inj_time_df[inj_time_df['tc'].isin(injs)].reset_index(drop=True)

for i in range(len(fits_combined_df)):
    for j in range(len(inj_time_df)):
        if fits_combined_df['time'][i] > inj_time_df['tc'][j] - 0.5 and fits_combined_df['time'][i] < inj_time_df['tc'][j] + 0.5:
            fits_combined_df.at[i, 'injection_index'] = inj_time_df['injection_index'][j]
            break
# --------------------------------------------------------

# --------------------------------------------------------
# Reset inj_time_df to be used again for the old file
inj_time_df = inj_file_df.loc[:, ['injection_index', 'tc']]
old_combined_df = old_combined_df.sort_values(by='time')

old_filter = []
injs = []
for time in set(old_combined_file['time']):
    for inj in set(inj_file_df['tc'][:]):
        if time > inj - 0.5 and time < inj + 0.5:
            old_filter.append(time)
            injs.append(inj)
            break

old_combined_df = old_combined_df[old_combined_df['time'].isin(old_filter)].reset_index(drop=True)
inj_time_df = inj_time_df[inj_time_df['tc'].isin(injs)].reset_index(drop=True)

for i in range(len(old_combined_df)):
    for j in range(len(inj_time_df)):
        if old_combined_df['time'][i] > inj_time_df['tc'][j] - 0.5 and old_combined_df['time'][i] < inj_time_df['tc'][j] + 0.5:
            old_combined_df.at[i, 'injection_index'] = inj_time_df['injection_index'][j]
            break
# --------------------------------------------------------

# --------------------------------------------------------

print("Fits injs found: ", len(fits_combined_df))
print("Old injs found: ", len(old_combined_df))

fits_indices = fits_combined_df['injection_index']
old_indices = old_combined_df['injection_index']

seen_by_both = np.intersect1d(fits_indices, old_indices)

print(len(seen_by_both))

# --------------------------------------------------------
# Write new hdf files with the filters and indices in
fits_file_name = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/vt_calculation/fits_coinc_combined_filtered.hdf'
old_file_name = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/vt_calculation/old_coinc_combined_filtered.hdf'

# with h5py.File(fits_file_name, 'w') as hdf_file:

#     for dataset_name in fits_combined_df.keys():
#         current_dataset = fits_combined_df[dataset_name][:]
#         hdf_file.create_dataset(dataset_name, data=current_dataset)

# with h5py.File(old_file_name, 'w') as hdf_file:

#     for dataset_name in old_combined_df.keys():
#         current_dataset = old_combined_df[dataset_name][:]
#         hdf_file.create_dataset(dataset_name, data=current_dataset)

fits_combined_file.close()
old_combined_file.close()
inj_file.close()
# --------------------------------------------------------

kept_keys = ['H1_chisq', 'H1_psd_var_val', 'H1_sg_chisq', 'H1_sigmasq',
             'H1_snr', 'L1_chisq', 'L1_psd_var_val', 'L1_sg_chisq',
             'L1_sigmasq', 'L1_snr', 'ifar_exclusive', 'injection_index',
             'network_snr', 'stat']

fits_combined_df = fits_combined_df[kept_keys]
old_combined_df = old_combined_df[kept_keys]

joined_df = pd.merge(fits_combined_df, old_combined_df, on='injection_index', suffixes=('_F', '_O'))

selected_keys = ['injection_index', 'ifar_exclusive_F', 'ifar_exclusive_O']
print(joined_df.loc[:, selected_keys])

better_ifar = (joined_df['ifar_exclusive_F'] - joined_df['ifar_exclusive_O']) > 0
worse_ifar = (joined_df['ifar_exclusive_F'] - joined_df['ifar_exclusive_O']) < 0
print("Num Better: ", sum(better_ifar))
print("Num Worse: ", sum(worse_ifar))

selected_keys = ['injection_index', 'ifar_exclusive_F', 'ifar_exclusive_O', 'ifar_diff']
joined_df_fits_worse = joined_df[worse_ifar]
joined_df_fits_worse['ifar_diff'] = joined_df_fits_worse['ifar_exclusive_F'] - joined_df_fits_worse['ifar_exclusive_O']
joined_df_fits_worse = joined_df_fits_worse.loc[:, selected_keys].sort_values(by='ifar_diff', ascending=True)

joined_df_fits_worse.to_csv('fits_worse.csv')


# Plots
if False:
    fig = plt.figure(figsize=(7, 7))
    plt.xlabel('Old Stat')
    plt.ylabel('Fits & PSD Var')
    plt.plot([1e-5, 1e5], [1e-5, 1e5], linestyle=':', color='k')
    plt.vlines(1, 1e-5, 1e5, linestyle='--', color='r', alpha=0.5)
    plt.hlines(1, 1e-5, 1e5, linestyle='--', color='r', alpha=0.5)
    plt.xlim(1e-5, 1e5)
    plt.ylim(1e-5, 1e5)
    plt.scatter(joined_df['ifar_exclusive_O'], joined_df['ifar_exclusive_F'], marker='x', s=5)
    plt.loglog()
    plt.savefig('fits_vs_old.png')
    plt.close()

    # Plot VT ratios
    ifar_lims = np.logspace(-4, 4, 1000)
    ratios = []
    for ifar_lim in ifar_lims:
        old_ifars_lims = joined_df['ifar_exclusive_O'][joined_df['ifar_exclusive_O'] > ifar_lim]
        fits_psd_ifars_lims = joined_df['ifar_exclusive_F'][joined_df['ifar_exclusive_F'] > ifar_lim]

        ratio = len(fits_psd_ifars_lims) / len(old_ifars_lims)
        ratios.append(ratio)

    # print(ratios)
    fig = plt.figure(figsize=(8, 6))
    plt.plot(ifar_lims, ratios)
    plt.xlabel('IFAR (yr)')
    plt.ylabel('VT ratio (Fits / Old)')
    plt.vlines(1, 0, 2, linestyle=':', color='blue', alpha=0.5)
    plt.hlines(1, 1e-4, 1e4, linestyle='--', color='r', alpha=0.5)
    plt.xlim(1e-4, 1e4)
    plt.ylim(0.8, 2)
    plt.grid(True)
    plt.xscale('log')
    plt.savefig('ratio.png')
    plt.close()
