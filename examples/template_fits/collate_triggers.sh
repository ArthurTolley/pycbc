#!/bin/bash

# Collect the triggers and merge them into one file

start_date='2020-01-06'
end_date='2020-01-12'
num_days=7 # Make sure you get this correct, this INCLUDES the start date
trigger_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/output/'
output_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/'
bank_file='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1L1-BBHBANK-1235750266-2415776.hdf'

python collate_live_triggers.py \
    --start-date ${start_date} \
    --end-date ${end_date} \
    --trigger-dir ${trigger_dir} \
    --output-dir ${output_dir} \
    --ifos 'H1' 'L1'\

start_date="${start_date//-/_}"
collated_triggger_file=${output_dir}'H1L1-Live-'${start_date}-${num_days}.hdf

# H1
pycbc_fit_sngls_by_template \
  --fit-function exponential  \
  --stat-threshold 6.0 \
  --prune-param mtotal \
  --log-prune-param  \
  --prune-bins 2 \
  --prune-number 2 \
  --sngl-ranking newsnr_sgveto \
  --ifo H1 \
  --trigger-file ${collated_triggger_file} \
  --bank-file ${bank_file} \
  --output ${output_dir}H1-test-coeffs.hdf \
  --verbose

pycbc_fit_sngls_over_multiparam \
  --verbose \
  --template-fit-file ${output_dir}H1-test-coeffs.hdf \
  --bank-file ${bank_file} \
  --output ${output_dir}H1-multiparam.hdf \
  --fit-param template_duration chi_eff eta \
  --f-lower 15.0 \
  --log-param True False False \
  --smoothing-width 0.4 0.2 0.08 \

# L1
pycbc_fit_sngls_by_template \
  --fit-function exponential  \
  --stat-threshold 6.0 \
  --prune-param mtotal \
  --log-prune-param  \
  --prune-bins 2 \
  --prune-number 2 \
  --sngl-ranking newsnr_sgveto \
  --ifo L1 \
  --trigger-file ${collated_triggger_file} \
  --bank-file ${bank_file} \
  --output ${output_dir}L1-test-coeffs.hdf \
  --verbose

pycbc_fit_sngls_over_multiparam \
  --verbose \
  --template-fit-file ${output_dir}L1-test-coeffs.hdf \
  --bank-file ${bank_file} \
  --output ${output_dir}L1-multiparam.hdf \
  --fit-param template_duration chi_eff eta \
  --f-lower 15.0 \
  --log-param True False False \
  --smoothing-width 0.4 0.2 0.08 \
