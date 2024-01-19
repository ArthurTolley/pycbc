import h5py
import numpy
import os
import logging
import timeit
import argparse
from datetime import datetime, timedelta


parser = argparse.ArgumentParser()
parser.add_argument('--start-date', type=str, required=False,
                    help='The first day of triggers you want to collate.'
                         'If no end date is given, the start date is the '
                         'only day.')
parser.add_argument('--num-days', type=int, required=False,
                    help='The number of days after (and including) the start '
                    'date to collate triggers from.')
parser.add_argument('--end-date', type=str, required=False,
                    help='The final day of triggers to collect. If no end '
                         'is provided then only the start day is used.')
parser.add_argument('--trigger-dir', type=str, required=False,
                    help='The directory containing all of the PyCBC Live '
                         'trigger files. The directory must contain sub-'
                         'directories with naming schemes "YYYY-MM-DD".'
                         'The trigger files must be of the formate: '
                         '"H1L1-Live-GPSTIME-INCREMENT.hdf". Currently '
                         'only H1 and L1 coincidences are supported.')
parser.add_argument('--trigger-file-list', type=str, required=False,
                    help='A file containing all the trigger files you '
                    ' would like to collate.')
parser.add_argument('--output-dir', type=str, required=True,
                    help='The directory to write the collated trigger file '
                         'to. The file will be named with the following '
                         'format: "H1L1-Live-STARTDAY-NUMDAYS.hdf"')
parser.add_argument('--output-file', type=str,
                    help='The name of the output file you want to create.')
parser.add_argument('--ifos', type=str, required=True, nargs='+',
                    help='The detectors to extract triggers for in the '
                         'trigger files. Currently H1 and L1 supported.')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)

start = timeit.default_timer()

if args.trigger_file_list:
    print(args.trigger_file_list)
    trigger_files = numpy.loadtxt(args.trigger_file_list, delimiter=',', dtype=str)

else:
    # Convert dates to datetime to get the days array
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()


    # Find the correct end_date using either end_date or num_days
    if args.end_date and args.num_days:
        print('Please provide only one of end_date or num_days.')
    elif args.end_date:
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
    elif args.num_days:
        num_days = timedelta(days=args.num_days - 1)
        end_date = start_date + num_days
    else:
        print('Either end_date or num_days must be provided.')

    # Create the days array
    days = []
    delta = timedelta(days=1)

    # Loop through the days and add each date to the list
    current_date = start_date
    while current_date <= end_date:
        days.append(current_date)
        current_date += delta

    # Convert to strings in a list
    days = [str(date).replace('-', '_') for date in days]
    num_days = str(len(days))

    trigger_files = [
        os.path.join(args.trigger_dir, day, trigger_file)
        for day in days
        for trigger_file in os.listdir(os.path.join(args.trigger_dir, day))
    ]



logging.info(f" {len(trigger_files)} files found")

if args.output_file:
    output_file = args.output_dir + args.output_file
else:
    ifo_string = "".join(args.ifos)
    print(ifo_string)
    output_file = args.output_dir + f'{ifo_string}-Live-' + days[0] + '-' + num_days + '.hdf'

logging.info(f" Creating a file at: {output_file}")
with h5py.File(output_file, 'a') as destination:
    # Create the ifo groups in the trigger file
    for ifo in args.ifos:
        if ifo not in destination:
            destination.create_group(ifo)

    file_count = 0
    for source_file in trigger_files:
        file_count += 1
        trigger_file = os.path.basename(source_file)
        if not (trigger_file.endswith('.hdf') and trigger_file.startswith('H1L1-Live')):
            continue

        start_time = float(trigger_file.split('-')[2])
        duration = float(trigger_file.split('-')[3][:-4])
        end_time = start_time + duration

        if file_count % 100 == 0:
            logging.info(f" Files appended: {file_count}/{len(trigger_files)}")

        with h5py.File(source_file, 'r') as source:
            for ifo in args.ifos:
                triggers = source[ifo]
                if ('approximant' not in triggers) or (len(triggers['approximant']) == 0):
                        continue

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
    for ifo in args.ifos:
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


        # Chisq is saved as reduced chisq for live triggers but offline
        #  code required original chisq. This converts it back.
        tmpval = triggers['chisq'][:] * (2 * triggers['chisq_dof'][:] - 2)
        triggers['chisq'][:] = tmpval

        # Datasets which need region references:
        region_ref_datasets = ('chisq_dof', 'chisq', 'coa_phase',
                               'end_time', 'sg_chisq', 'snr',
                               'template_duration', 'sigmasq')
        if 'psd_var_val' in triggers.keys():
            region_ref_datasets += ('psd_var_val',)
        start_boundaries = template_boundaries
        end_boundaries = numpy.roll(start_boundaries, -1)
        end_boundaries[-1] = len(template_ids)

        for dataset in region_ref_datasets:
            dset = triggers[dataset][:]
            refs = []

            for i in range(len(template_boundaries)):
                refs.append(triggers[dataset].regionref[start_boundaries[i]:end_boundaries[i]])

            triggers.create_dataset\
            (dataset + '_template', data=refs, dtype=h5py.special_dtype(ref=h5py.RegionReference))

end = timeit.default_timer()
total_time = float(end - start)
logging.info(f" Time taken: {total_time}")
