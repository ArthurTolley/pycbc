import h5py
import numpy as np
import os

# Directory containing all the PyCBC Live triggers
triggers_dir = '/home/pycbc.live/analysis/prod/o4/full_bandwidth/cit/triggers/'

# A random week in June
#week = ['2023_06_20', '2023_06_21', '2023_06_22', '2023_06_23', '2023_06_24', '2023_06_25', '2023_06_26']
week = ['2023_06_20']

# Probably combine them by single days first
day_file_dir = '/home/arthur.tolley/PyCBC_changes/live_stat/trigger_files/'

# Example file name:
#  '/home/pycbc.live/analysis/prod/o4/full_bandwidth/cit/triggers/2023_04_17/H1L1-Live-1365767992.069336-8.hdf'

for day in week:
    day_file = day_file_dir + day + '.hdf'

    triggers = os.listdir(triggers_dir + day)

    for file in triggers:
        if not (file.endswith('.hdf') and file.startswith('H1L1-Live')):
            continue

        source_file = os.path.join(triggers_dir, day, file)
        duration = float(file[-5:-4])
        start_time = float(file[-23:-6])
        end_time = start_time + duration

        with h5py.File(source_file, 'r') as source:
            with h5py.File(day_file, 'a') as destination:

                h1_trigs = source['H1']
                l1_trigs = source['L1']

                # Create the ifo groups in the trigger file
                if 'H1' not in destination:
                    destination.create_group('H1')
                if 'L1' not in destination:
                    destination.create_group('L1')

                if len(destination['H1'].keys()) == 0:
                    for name, dataset in h1_trigs.items():
                        destination['H1'].create_dataset(name, data=dataset, chunks=True, maxshape=(None,))

                else:
                    for name in h1_trigs.keys():
                        if name in destination['H1']:
                            if destination['H1'][name].shape[0] == 0:
                                # Skip resizing or appending if the dataset is empty
                                continue
                            if h1_trigs[name].shape[0] == 0:
                                continue
                            # Append new data to existing dataset in destination
                            destination['H1'][name].resize((destination['H1'][name].shape[0] + h1_trigs[name].shape[0]), axis=0)
                            destination['H1'][name][-h1_trigs[name].shape[0]:] = h1_trigs[name]

                if len(destination['L1'].keys()) == 0:
                    for name, dataset in l1_trigs.items():
                        destination['L1'].create_dataset(name, data=dataset, chunks=True, maxshape=(None,))

                else:
                    for name in l1_trigs.keys():
                        if name in destination['L1']:
                            if destination['L1'][name].shape[0] == 0:
                                # Skip resizing or appending if the dataset is empty
                                continue
                            if l1_trigs[name].shape[0] == 0:
                                continue
                            # Append new data to existing dataset in destination
                            destination['L1'][name].resize((destination['L1'][name].shape[0] + l1_trigs[name].shape[0]), axis=0)
                            destination['L1'][name][-l1_trigs[name].shape[0]:] = l1_trigs[name]


                for attr_name, attr_value in source.attrs.items():
                    destination.attrs[attr_name] = attr_value

                # Create or get the '/search' subgroup within 'H1' and 'L1'
                if 'search' not in destination['H1']:
                    destination['H1'].create_group('search')
                if 'search' not in destination['L1']:
                    destination['L1'].create_group('search')

                # Create or append 'start_time' and 'end_time' datasets within the '/search' group
                if 'start_time' in destination['H1']['search']:
                    destination['H1']['search']['start_time'].resize((destination['H1']['search']['start_time'].shape[0] + 1), axis=0)
                    destination['H1']['search']['start_time'][-1] = start_time
                else:
                    destination['H1']['search'].create_dataset('start_time', chunks=True, data=np.array([start_time]), maxshape=(None,))

                if 'end_time' in destination['H1']['search']:
                    destination['H1']['search']['end_time'].resize((destination['H1']['search']['end_time'].shape[0] + 1), axis=0)
                    destination['H1']['search']['end_time'][-1] = end_time
                else:
                    destination['H1']['search'].create_dataset('end_time', chunks=True, data=np.array([end_time]), maxshape=(None,))

                if 'start_time' in destination['L1']['search']:
                    destination['L1']['search']['start_time'].resize((destination['L1']['search']['start_time'].shape[0] + 1), axis=0)
                    destination['L1']['search']['start_time'][-1] = start_time
                else:
                    destination['L1']['search'].create_dataset('start_time', chunks=True, data=np.array([start_time]), maxshape=(None,))

                if 'end_time' in destination['L1']['search']:
                    destination['L1']['search']['end_time'].resize((destination['L1']['search']['end_time'].shape[0] + 1), axis=0)
                    destination['L1']['search']['end_time'][-1] = end_time
                else:
                    destination['L1']['search'].create_dataset('end_time', chunks=True, data=np.array([end_time]), maxshape=(None,))


