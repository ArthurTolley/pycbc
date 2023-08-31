import logging
import numpy as np
import h5py

input_file = '/home/arthur.tolley/PyCBC_changes/live_stat/trigger_files/test/2023_06_20.hdf'
#ifos = ['H1', 'L1']
ifos = ['L1']

# Load in the trigger files
with h5py.File(input_file, 'a') as input:
    for ifo in ifos:
        # Grab the ifo you want
        triggers = input[ifo]
        all_tids = triggers['template_id'][:]

        # 17.4 seconds to do this
        tids = np.arange(np.max(all_tids) + 1, dtype=int)

        sorted_indices = np.argsort(all_tids)
        sorted_template_ids = all_tids[sorted_indices]
        unique_template_ids, template_id_counts = np.unique(sorted_template_ids, return_counts=True)
        index_boundaries = np.cumsum(template_id_counts)
        template_boundaries = np.insert(index_boundaries, 0, 0)[:-1]

        # Re-running purposes, comment out otherwise
        #del triggers['template_boundaries']
        triggers['template_boundaries'] = template_boundaries

        # Sort other datasets by template_id so it makes sense:
        # Datasets with the same length as the number of triggers:
        #   Approximant, chisq, chisq_dof, coa_phase, end_time, f_lower
        #   mass_1, mass_2, sg_chisq, sigmasq, snr, spin1z, spin2z,
        #   template_duration, template_hash, template_id
        for key in triggers.keys():
            if len(triggers[key]) == len(all_tids):
                logging.info(f'Sorting {key}')
                sorted_key = triggers[key][:][sorted_indices]
                triggers[key][:] = sorted_key

