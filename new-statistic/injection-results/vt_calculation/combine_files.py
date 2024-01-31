import pycbc.io
import h5py

bank_file_path = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/run-files/H1L1-BBHBANK-1235750266-2415776.hdf'

fits_coinc_statmap_path = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-fits-psd-var/statmap/H1L1-STATMAP_no_injs.hdf'
fits_coinc_inj_statmap_path = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-fits-psd-var/statmap/H1L1-STATMAP_INJ_with_injs.hdf'
fits_sngl_files_H1_with = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-fits-psd-var/trigger-merges/H1_with_injs.hdf'
fits_sngl_files_L1_with = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-fits-psd-var/trigger-merges/L1_with_injs.hdf'


old_coinc_statmap_path = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-old-stat/statmap/H1L1-STATMAP_no_injs.hdf'
old_coinc_inj_statmap_path = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-old-stat/statmap/H1L1-STATMAP_INJ_with_injs.hdf'
old_sngl_files_H1_with = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-old-stat/trigger-merges/H1_with_injs.hdf'
old_sngl_files_L1_with = '/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/searches/joint-old-stat/trigger-merges/L1_with_injs.hdf'


# fits_combined_file = pycbc.io.hdf.ForegroundTriggers(coinc_file = fits_coinc_inj_statmap_path,
#                                                      bank_file = bank_file_path,
#                                                      sngl_files=[fits_sngl_files_H1_with, fits_sngl_files_L1_with])


# fits_combined_file.to_coinc_hdf_object('fits_coinc_combined.hdf')

old_combined_file = pycbc.io.hdf.ForegroundTriggers(coinc_file = old_coinc_inj_statmap_path,
                                                     bank_file = bank_file_path,
                                                     sngl_files=[old_sngl_files_H1_with, old_sngl_files_L1_with])


old_combined_file.to_coinc_hdf_object('old_coinc_combined.hdf')