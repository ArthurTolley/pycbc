import matplotlib.pyplot as plt
import numpy
import h5py
import pandas as pd

# Load in the hdfinjfind files
old_hdfinjfind = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-old-stat/hdfinjfind/H1L1-HDFINJFIND_BBH_RATESINJ_INJECTIONS-1262995020-600000.hdf', 'r')
fits_psd_hdfinjfind = h5py.File('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-fits-psd-var/hdfinjfind/H1L1-HDFINJFIND_BBH_RATESINJ_INJECTIONS-1262995020-600000.hdf', 'r')

print("Number of injections found near a trigger:")
print("Old Stat: ", len(old_hdfinjfind['found_after_vetoes']['ifar_exc'][:]))
print("Fits + PSD Var: ", len(fits_psd_hdfinjfind['found_after_vetoes']['ifar_exc'][:]))
print("")

ifar_lim = 0.0

old_ifars = old_hdfinjfind['found_after_vetoes']['ifar_exc'][:][old_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]
old_idxs = old_hdfinjfind['found_after_vetoes']['injection_index'][:][old_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]
old_stat = old_hdfinjfind['found_after_vetoes']['stat'][:][old_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]


fits_psd_ifars = fits_psd_hdfinjfind['found_after_vetoes']['ifar_exc'][:][fits_psd_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]
fits_psd_idxs = fits_psd_hdfinjfind['found_after_vetoes']['injection_index'][:][fits_psd_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]
fits_psd_stat = fits_psd_hdfinjfind['found_after_vetoes']['stat'][:][fits_psd_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]

ifar_lims = numpy.logspace(-4, 4, 1000)  # Add the desired ifar_lim values here
ratios = []
for ifar_lim in ifar_lims:
    old_ifars_lims = old_hdfinjfind['found_after_vetoes']['ifar_exc'][:][old_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]
    fits_psd_ifars_lims = fits_psd_hdfinjfind['found_after_vetoes']['ifar_exc'][:][fits_psd_hdfinjfind['found_after_vetoes']['ifar_exc'][:] > ifar_lim]

    ratio = len(fits_psd_ifars_lims) / len(old_ifars_lims)
    ratios.append(ratio)

# print(ratios)
plt.plot(ifar_lims, ratios)
plt.xlabel('ifar_lim')
plt.ylabel('ratio')
plt.xscale('log')
plt.savefig('./plots/ratio.png')
plt.close()

# print(f"Number of injections found with ifar > {ifar_lim}:")
# print("Old Stat: ", len(old_ifars))
# print("Fits + PSD Var: ", len(fits_psd_ifars))
# print("")

common_idxs = list(set(old_idxs).intersection(set(fits_psd_idxs)))
print(f"Number injections found by both old-stat and fits-psd-var with ifar > {ifar_lim}:")
print(len(common_idxs))
print("")



old_stat = pd.DataFrame({'ifar': old_ifars, 'idx': old_idxs, 'stat': old_stat})
fits_psd = pd.DataFrame({'ifar': fits_psd_ifars, 'idx': fits_psd_idxs, 'stat': fits_psd_stat})

old_stat_commons = old_stat[old_stat['idx'].isin(common_idxs)].reset_index()
fits_psd_commons = fits_psd[fits_psd['idx'].isin(common_idxs)].reset_index()

# print("Checks:")
# print(len(old_stat_commons))
# print(len(fits_psd_commons))
# print(len(common_idxs))
# print("")

# Plot the raw change in IFAR
change = fits_psd_commons['ifar'] - old_stat_commons['ifar']
pos_change = change[change > 0]
neg_change = change[change < 0]
pos_idxs = old_stat_commons['idx'][change > 0]
neg_idxs = old_stat_commons['idx'][change < 0]


fig = plt.figure(figsize=(10, 6))

# Change the color of the points based on the value of `change`
plt.plot(neg_idxs, neg_change, 'ro')
plt.plot(pos_idxs, pos_change, 'go')

# plt.xlabel('Injection Index')
# plt.ylabel('Change in IFAR')
# plt.title(f'Increased IFAR: {len(change[change > 0])}       Decreased IFAR: {len(change[change < 0])}')
# plt.grid(True)
# plt.savefig('./plots/changed_ifars.png')
# plt.close()

print("Changed ifars:")
print("Increase: ", len(change[change > 0]))
print("Decrease: ", len(change[change < 0]))
print("")
print("Changed ifars >100/-100:")
print("Increase: ", len(change[change > 100]))
print("Decrease: ", len(change[change < -100]))

# Plot the raw IFARs
# plt.scatter(common_idxs, old_stat_commons['ifar'], label='old')
# plt.scatter(common_idxs, fits_psd_commons['ifar'], label='fits_psd')
# plt.legend()
# plt.grid(True)
# plt.savefig('./plots/ifars.png')
# plt.close()

# Plot histograms

# fig = plt.figure(figsize=(10, 6))
# plt.hist(pos_change, bins=20, label='positive change', color='g')
# plt.hist(neg_change, bins=20, label='negative change', color='r')
# plt.legend()
# plt.savefig('./plots/hist.png')
# plt.close()

# plt.hist(pos_change[pos_change < 100], bins=10, label='positive change', color='g')
# plt.hist(neg_change[neg_change > -100], bins=10, label='negative change', color='r')
# plt.legend()
# plt.savefig('./plots/trunc_hist.png')
# plt.close()

# plt.hist(old_stat_commons['ifar'], bins=50)
# plt.xlabel('IFAR')
# plt.savefig('./plots/old_stat_ifar_hist.png')
# plt.close()

# plt.hist(fits_psd_commons['ifar'], bins=50)
# plt.xlabel('IFAR')
# plt.savefig('./plots/fits_ifar_hist.png')
# plt.close()

# plt.hist(old_stat_commons['stat'], bins=50)
# plt.xlabel('STAT')
# plt.savefig('./plots/old_stat_stat_hist.png')
# plt.close()

# plt.hist(fits_psd_commons['stat'], bins=50)
# plt.xlabel('STAT')
# plt.savefig('./plots/fits_stat_hist.png')
# plt.close()

# ---------------------------------------------
# STAT vs IFAR
# plt.scatter(old_stat_commons['ifar'], old_stat_commons['stat'], label='old')
# plt.scatter(fits_psd_commons['ifar'], fits_psd_commons['stat'], label='fits_psd')
# plt.xlabel('IFAR')
# plt.ylabel('STAT')
# plt.grid(True)
# plt.legend()
# plt.savefig('./plots/stat_vs_ifar.png')
# plt.close()

# IFAR vs STAT
# plt.scatter(old_stat_commons['stat'], old_stat_commons['ifar'], label='old', marker='x', s=5)
# plt.scatter(fits_psd_commons['stat'], fits_psd_commons['ifar'], label='fits_psd', marker='^', s=5)
# plt.xlabel('STAT')
# plt.ylabel('IFAR')
# plt.grid(True)
# plt.legend()
# plt.savefig('./plots/ifar_vs_stat.png')
# plt.close()

# IFAR vs IFAR
fig = plt.figure(figsize=(7, 7))
plt.xlabel('Old')
plt.ylabel('Fits')
plt.plot([1e-5, 1e5], [1e-5, 1e5], linestyle=':', color='k')
plt.vlines(1, 1e-5, 1e5, linestyle='--', color='r')
plt.hlines(1, 1e-5, 1e5, linestyle='--', color='r')
plt.xlim(1e-5, 1e5)
plt.ylim(1e-5, 1e5)
plt.scatter(old_stat_commons['ifar'], fits_psd_commons['ifar'], label='old vs fits_psd', marker='x', s=5)
plt.loglog()
plt.savefig('./plots/fits_vs_old.png')
plt.close()

# print(numpy.sort(neg_change))

change = fits_psd_commons['ifar'] - old_stat_commons['ifar']
pos_change = change[change > 0]
neg_change = change[change < 0]

# all_ifars = 
