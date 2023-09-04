import h5py
import numpy
import os
import logging
import timeit

logging.basicConfig(level=logging.INFO)

start = timeit.default_timer()

# Select the days you want to make a file from
# For a single day, just list that single day
#days = ['2023_06_20']
#days = ['2023_06_20', '2023_06_21', '2023_06_22', '2023_06_23', '2023_06_24', '2023_06_25', '2023_06_26']
#days = ['2023_07_31']
days = ['2023_07_31', '2023_08_01', '2023_08_02', '2023_08_03', '2023_08_04', '2023_08_05', '2023_08_06']
num_days = str(len(days))

# Directory containing all the PyCBC Live triggers
triggers_dir = '/home/pycbc.live/analysis/prod/o4/full_bandwidth/cit/triggers/'
trigger_files = [os.path.join(triggers_dir, day, trigger_file) for day in days for trigger_file in os.listdir(triggers_dir + day)]
logging.info(f" {len(trigger_files)} files found")

# Probably combine them by single days first
output_file_dir = '/home/arthur.tolley/PyCBC_changes/live_stat/trigger_files/'

# Example file name:
#  '/home/pycbc.live/analysis/prod/o4/full_bandwidth/cit/triggers/2023_04_17/H1L1-Live-1365767992.069336-8.hdf'

ifos = ['L1', 'H1']

output_file = output_file_dir + 'H1L1-Live-' + days[0] + '-' + num_days + '.hdf'
logging.info(f" Creating a file at: {output_file}")
with h5py.File(output_file, 'a') as destination:
    # Create the ifo groups in the trigger file
    for ifo in ifos:
        if ifo not in destination:
            destination.create_group(ifo)

    file_count = 0
    for source_file in trigger_files:
        file_count += 1
        trigger_file = os.path.basename(source_file)
        if not (trigger_file.endswith('.hdf') and trigger_file.startswith('H1L1-Live')):
            continue

        duration = float(trigger_file[-5:-4])
        start_time = float(trigger_file[-23:-6])
        end_time = start_time + duration

        if file_count % 100 == 0:
            logging.info(f" Files appended: {file_count}/{len(trigger_files)}")

        with h5py.File(source_file, 'r') as source:
            for ifo in ifos:
                triggers = source[ifo]

                for name, dataset in triggers.items():
                    if name in destination[ifo]:
                        if triggers[name].shape[0] == 0:
                            continue
                        # Append new data to existing dataset in destination
                        destination[ifo][name].resize((destination[ifo][name].shape[0] + triggers[name].shape[0]), axis=0)
                        destination[ifo][name][-triggers[name].shape[0]:] = triggers[name]
                    else:
                        destination[ifo].create_dataset(name, data=dataset, chunks=True, maxshape=(None,))

                for attr_name, attr_value in source.attrs.items():
                    destination.attrs[attr_name] = attr_value

                # Create or get the '/search' subgroup within 'H1' and 'L1'
                if 'search' not in destination[ifo]:
                    destination[ifo].create_group('search')

                # Create or append 'start_time' and 'end_time' datasets within the '/search' group
                if 'start_time' in destination[ifo]['search']:
                    destination[ifo]['search']['start_time'].resize((destination[ifo]['search']['start_time'].shape[0] + 1), axis=0)
                    destination[ifo]['search']['start_time'][-1] = start_time
                else:
                    destination[ifo]['search'].create_dataset('start_time', chunks=True, data=numpy.array([start_time]), maxshape=(None,))

                if 'end_time' in destination[ifo]['search']:
                    destination[ifo]['search']['end_time'].resize((destination[ifo]['search']['end_time'].shape[0] + 1), axis=0)
                    destination[ifo]['search']['end_time'][-1] = end_time
                else:
                    destination[ifo]['search'].create_dataset('end_time', chunks=True, data=numpy.array([end_time]), maxshape=(None,))

# Add all the template boundaries
with h5py.File(output_file, 'a') as output:
    for ifo in ifos:
        logging.info(f" Adding template boundaries for {ifo}")
        # Grab the ifo you want
        triggers = output[ifo]
        try:
            template_ids = triggers['template_id'][:]
        except:
            logging.info(f"  No triggers for {ifo}, skipping")
            continue

        # 17.4 seconds to do this
        tids = numpy.arange(numpy.max(template_ids) + 1, dtype=int)

        sorted_indices = numpy.argsort(template_ids)
        sorted_template_ids = template_ids[sorted_indices]
        unique_template_ids, template_id_counts = numpy.unique(sorted_template_ids, return_counts=True)
        index_boundaries = numpy.cumsum(template_id_counts)
        template_boundaries = numpy.insert(index_boundaries, 0, 0)[:-1]

        # Re-running purposes, comment out otherwise
        #del triggers['template_boundaries']
        triggers['template_boundaries'] = template_boundaries

        # Sort other datasets by template_id so it makes sense:
        # Datasets with the same length as the number of triggers:
        #   Approximant, chisq, chisq_dof, coa_phase, end_time, f_lower
        #   mass_1, mass_2, sg_chisq, sigmasq, snr, spin1z, spin2z,
        #   template_duration, template_hash, template_id
        for key in triggers.keys():
            if len(triggers[key]) == len(template_ids):
                logging.info(f'  Sorting {key} by template id')
                sorted_key = triggers[key][:][sorted_indices]
                triggers[key][:] = sorted_key

        # Add the region references for sigmasq
        logging.info(f" Adding region references for {ifo}")
        sigmasq_dataset = triggers['sigmasq'][:]
        start_boundaries = template_boundaries
        end_boundaries = numpy.roll(start_boundaries, -1)
        end_boundaries[-1] = len(template_ids)

        refs = []

        for i in range(len(template_boundaries)):
            refs.append(triggers['sigmasq'].regionref[start_boundaries[i]:end_boundaries[i]])
        triggers.create_dataset\
            ('sigmasq' + '_template', data=refs,
                dtype=h5py.special_dtype(ref=h5py.RegionReference))

end = timeit.default_timer()
total_time = float(end - start)
logging.info(f" Time taken: {total_time}")
