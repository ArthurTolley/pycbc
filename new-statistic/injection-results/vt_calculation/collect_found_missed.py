import os
import h5py
import numpy as np
import pandas as pd

import pycbc.conversions as conv

old_stat = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/old-stat/hdfinjfind/'
fits_only = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/hdfinjfind/'
fits_psd_var ='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-psd-var/hdfinjfind/'

result_types = ['old_stat', 'fits_only', 'fits_psd_var']
search_names = ['bbh']
injtypes = {'bbh': ['BBH_RATESINJ']}
all_ifos = ['H1','L1']

injfind_dirs = {
'old_stat': old_stat,
'fits_only': fits_only,
'fits_psd_var': fits_psd_var,
}

injfind_files = {result: {search: {injtype: sorted([os.path.join(injfind_dirs[result], fname)
                                                    for fname in os.listdir(injfind_dirs[result])
                                                    if 'HDFINJFIND' in fname and injtype in fname])
                                   for injtype in injtypes[search]}
                          for search in search_names}
                 for result in result_types}

bbh_chunk_starts = np.array([float(1262995020)])

results_arrays = {injtype: {} for injtype in injtypes['bbh']}

inj_times = {}
inj_dist = {}
inj_mchirp = {}
net_opt_snr = {}
dec_opt_snr = {}
max_opt_snr = {}
inj_chunk = {}
for injtype in injtypes['bbh']:
    inj_times[injtype] = np.array([])
    inj_dist[injtype] = np.array([])
    inj_chunk[injtype] = np.array([])
    inj_mchirp[injtype] = np.array([])
    filelist = [f for f in injfind_files['fits_only']['bbh'][injtype]]
    for fname in filelist:
        ts = float(fname.split('-')[-2])
        chunkno = np.argmax(ts == bbh_chunk_starts)
        with h5py.File(fname,'r') as res_f:
            if 'tc' in res_f['injections'].keys():
                time = res_f['injections']['tc'][:]
            else:
                time = res_f['injections']['end_time'][:]
            mass1 = res_f['injections']['mass1'][:]
            mass2 = res_f['injections']['mass2'][:]
            dist = res_f['injections']['distance'][:]
        mchirp = conv.mchirp_from_mass1_mass2(mass1, mass2)
        inj_dist[injtype] = np.concatenate((inj_dist[injtype], dist))
        inj_times[injtype] = np.concatenate((inj_times[injtype], time))
        inj_mchirp[injtype] = np.concatenate((inj_mchirp[injtype], mchirp))
        inj_chunk[injtype] = np.concatenate((inj_chunk[injtype], np.ones_like(dist) * chunkno))

print("number of injections:")
print({injtype: len(inj_times[injtype]) for injtype in injtypes['bbh']})

inj_times_sort = {injtype: np.argsort(inj_times[injtype]) for injtype in injtypes['bbh']}
inj_times_sorted = {injtype: inj_times[injtype][inj_times_sort[injtype]]
                    for injtype in injtypes['bbh']}
dist_sorted = {injtype: inj_dist[injtype][inj_times_sort[injtype]]
                      for injtype in injtypes['bbh']}
inj_chunk_sorted = {injtype: inj_chunk[injtype][inj_times_sort[injtype]]
                    for injtype in injtypes['bbh']}
inj_mchirp_sorted = {injtype: inj_mchirp[injtype][inj_times_sort[injtype]]
                    for injtype in injtypes['bbh']}


for injtype in injtypes['bbh']:
    results_arrays[injtype]['inj_times'] = inj_times_sorted[injtype]
    results_arrays[injtype]['dist'] = dist_sorted[injtype]
    results_arrays[injtype]['injection_chunk'] = inj_chunk_sorted[injtype]
    results_arrays[injtype]['inj_mchirp'] = inj_mchirp_sorted[injtype]
    for result in result_types:
        results_arrays[injtype][result + '_bbh_ifar'] = np.zeros_like(inj_times_sorted[injtype])
        results_arrays[injtype][result + '_bbh_triggered'] = np.zeros_like(inj_times_sorted[injtype], dtype='S6')
        for fname in injfind_files[result]['bbh'][injtype]:
            with h5py.File(fname,'r') as f:
                if 'tc' in f['injections'].keys():
                    time = f['injections']['tc'][:]
                else:
                    time = f['injections']['end_time'][:]
                inj_idx = f['found_after_vetoes']['injection_index'][:]
                recovered_ifar = f['found_after_vetoes']['ifar_exc'][:]
                recovered_as_arr = zip(*[f['found_after_vetoes'][ifo]['time'][:] > 0
                                             for ifo in all_ifos])
            recovered_ifar = np.minimum(recovered_ifar, np.ones_like(recovered_ifar) * 5e4)
            ss = np.searchsorted(results_arrays[injtype]['inj_times'], time)
            results_arrays[injtype][result + '_bbh_ifar'][ss[inj_idx]] = recovered_ifar
            recovered_as = [''.join([ifo for ifo, ra in zip(all_ifos, raa) if ra])
                                              for raa in recovered_as_arr]
            results_arrays[injtype][result + '_bbh_triggered'][ss[inj_idx]] = recovered_as

for result in result_types:
    for injtype in injtypes['bbh']:
        recovered_ifars = []
        for search in ['bbh']:
            ifar_key = result + '_' + search + '_ifar'
            if ifar_key not in results_arrays[injtype]: continue
            recovered_ifars.append(results_arrays[injtype][ifar_key])

        if len(recovered_ifars) == 1:
            results_arrays[injtype][result + '_best_ifar'] = recovered_ifars[0]
        else:
            results_arrays[injtype][result + '_best_ifar'] = np.array(recovered_ifars).sum(axis=0)

for injtype in injtypes['bbh']:
    print({k: len(results_arrays[injtype][k]) for k in results_arrays[injtype].keys()})
    pddata = pd.DataFrame(data=results_arrays[injtype])
    pddata.to_csv("%s_results.txt" % injtype)
