#!/bin/bash

gps_start_time=1386547220
gps_end_time=1387152024
trigger_files_loc='/home/arthur.tolley/pycbc-live/mdc-fits/pycbc-live-triggers'
trigger_file_output_file=trigger_files.txt
trigger_file_output_location=/home/arthur.tolley/pycbc-live/mdc-fits/

bank_file='/home/pycbc.live/analysis/prod/o4/full_bandwidth/bank/O4_DESIGN_OPT_FLOW_HYBRID_BANK_O3_CONFIG.hdf'

# Get a list of the trigger files
python find_trigger_files.py \
    --gps-start-time ${gps_start_time} \
    --gps-end-time ${gps_end_time} \
    --trigger-file-loc ${trigger_files_loc} \
    --output-file ${trigger_file_output_file} \
    --output-location ${trigger_file_output_location}

# Collate the triggers into separate trigger files for each ifo
trigger_merge_output_dir='/home/arthur.tolley/pycbc-live/mdc-fits/fit-files/trigger-merges/'
trigger_file_list="${trigger_file_output_location}${trigger_file_output_file}"

H1_trigger_merge_output_file=H1_trigger_merge.hdf
python collate_live_triggers.py \
    --trigger-file-list ${trigger_file_list} \
    --output-dir ${trigger_merge_output_dir} \
    --output-file ${H1_trigger_merge_output_file} \
    --ifos 'H1' \

L1_trigger_merge_output_file=L1_trigger_merge
python collate_live_triggers.py \
    --trigger-file-list ${trigger_file_list} \
    --output-dir ${trigger_merge_output_dir} \
    --output-file ${L1_trigger_merge_output_file} \
    --ifos 'L1' \

# Create the template fits
# H1
H1_trigger_merge_file="${trigger_merge_output_dir}${H1_trigger_merge_output_file}"
H1_fits_output_dir='/home/arthur.tolley/pycbc-live/mdc-fits/fit-files/'
pycbc_fit_sngls_by_template \
  --fit-function exponential  \
  --stat-threshold 6.0 \
  --prune-param mtotal \
  --log-prune-param  \
  --prune-bins 2 \
  --prune-number 2 \
  --sngl-ranking newsnr_sgveto \
  --ifo H1 \
  --trigger-file ${H1_trigger_merge_file} \
  --bank-file ${bank_file} \
  --output "${H1_fits_output_dir}H1-test-coeffs.hdf" \
  --verbose

pycbc_fit_sngls_over_multiparam \
  --verbose \
  --template-fit-file "${H1_fits_output_dir}H1-test-coeffs.hdf" \
  --bank-file ${bank_file} \
  --output "${H1_fits_output_dir}H1-multiparam.hdf" \
  --fit-param template_duration chi_eff eta \
  --f-lower 15.0 \
  --log-param True False False \
  --smoothing-width 0.4 0.2 0.08 \

# L1
L1_trigger_merge_file="${trigger_merge_output_dir}${L1_trigger_merge_output_file}"
L1_fits_output_dir='/home/arthur.tolley/pycbc-live/mdc-fits/fit-files/'
pycbc_fit_sngls_by_template \
  --fit-function exponential  \
  --stat-threshold 6.0 \
  --prune-param mtotal \
  --log-prune-param  \
  --prune-bins 2 \
  --prune-number 2 \
  --sngl-ranking newsnr_sgveto \
  --ifo L1 \
  --trigger-file ${L1_trigger_merge_file} \
  --bank-file ${bank_file} \
  --output "${L1_fits_output_dir}L1-test-coeffs.hdf" \
  --verbose

pycbc_fit_sngls_over_multiparam \
  --verbose \
  --template-fit-file "${L1_fits_output_dir}L1-test-coeffs.hdf" \
  --bank-file ${bank_file} \
  --output "${L1_fits_output}L1-multiparam.hdf" \
  --fit-param template_duration chi_eff eta \
  --f-lower 15.0 \
  --log-param True False False \
  --smoothing-width 0.4 0.2 0.08 \
