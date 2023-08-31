import h5py
import numpy

input_file = '/home/arthur.tolley/PyCBC_changes/live_stat/trigger_files/test/2023_06_20.hdf'

with h5py.File(input_file, 'r+') as file:
    file = file['L1']
    template_ids = file['template_id'][:]
    template_boundaries = file['template_boundaries'][:]
    sigmasq_dataset = file['sigmasq'][:]

    try:
        del file['sigmasq_template']
    except:
        print('Nothing to delete')

    start_boundaries = template_boundaries
    end_boundaries = numpy.roll(start_boundaries, -1)
    end_boundaries[-1] = len(template_ids)

    refs = []

    for i in range(len(template_boundaries)):
        refs.append(file['sigmasq'].regionref[start_boundaries[i]:end_boundaries[i]])
    file.create_dataset\
        ('sigmasq' + '_template', data=refs,
            dtype=h5py.special_dtype(ref=h5py.RegionReference))
