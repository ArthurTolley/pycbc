# Converstion somehow
trigger_file = '/home/arthur.tolley/PyCBC_changes/live_stat/trigger_files/2023_06_20.hdf'
with h5py.File(trigger_file, 'r') as triggers:
    print(list(triggers['L1'].keys()))
    print(triggers['L1']['gates'])

# Offline triggers
trigger_file = '/home/pycbc.offline/O3/production/O3A_FINAL/ALL_TRIGGER_FILES/HYPERBANK/TRIGGER_MERGE/L1-HDF_TRIGGER_MERGE_FULL_DATA-1241724868-760282.hdf'
with h5py.File(trigger_file, 'r') as triggers:
    print(list(triggers['L1'].keys()))
    print(triggers['L1']['template_boundaries'][0:10])
    print(len(triggers['L1']['template_boundaries']))
    print(len(triggers['L1']['snr_template']))
    print(len(triggers['L1']['template_id']))
    print(triggers['L1']['template_id'][2450:2500])
    
# Converstion somehow
trigger_file = '/home/arthur.tolley/PyCBC_changes/live_stat/trigger_files/2023_06_20.hdf'
with h5py.File(trigger_file, 'r') as triggers:
    print(list(triggers['L1'].keys()))
    print(triggers['L1']['template_id'][:50])

    # Count occurrences of the specific template_id
    target_template_id = 0
    matching_indices = triggers['L1']['template_id'][:] == target_template_id
    num_matching_template_id = np.sum(matching_indices)

    print("Number of matching template_ids:", num_matching_template_id)