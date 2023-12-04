#!/bin/bash

# Collect the triggers and merge them into one file

# week 1 old no
#  H1 - Not
#  L1 - Not
# week 2 old no
#  H1 - Not
#  L1 - Not

# week 1 old with
#  H1 - Not
#  L1 - Not
# week 2 old with
#  H1 - Not
#  L1 - Not

# week 1 new no
#  H1 - Not
#  L1 - Not
# week 2 new no
#  H1 - Not
#  L1 - Not

# week 1 new with
#  H1 - Not
#  L1 - Not
# week 2 new with
#  H1 - Not
#  L1 - Not

# start_date='2020-01-06'
# end_date='2020-01-12'
# num_days=7 # Make sure you get this correct, this INCLUDES the start date
# trigger_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/output/'
output_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/'
# bank_file='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1L1-BBHBANK-1235750266-2415776.hdf'

stat=old
inj_state=with

trigger_file_list=/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/week_1_${stat}_${inj_state}.txt
output_dir=/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/

output_file=H1_week_1_${stat}_stat_${inj_state}_inj.hdf
python collate_live_triggers.py \
    --trigger-file-list ${trigger_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'H1' \

# output_file=L1_week_1_${stat}_stat_${inj_state}_inj.hdf
# python collate_live_triggers.py \
#     --trigger-file-list ${trigger_file_list} \
#     --output-dir ${output_dir} \
#     --output-file ${output_file} \
#     --ifos 'L1' \

# trigger_file_list=/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/week_2_${stat}_${inj_state}.txt

# output_file=H1_week_2_${stat}_stat_${inj_state}_inj.hdf
# python collate_live_triggers.py \
#     --trigger-file-list ${trigger_file_list} \
#     --output-dir ${output_dir} \
#     --output-file ${output_file} \
#     --ifos 'H1' \

# output_file=L1_week_2_${stat}_stat_${inj_state}_inj.hdf
# python collate_live_triggers.py \
#     --trigger-file-list ${trigger_file_list} \
#     --output-dir ${output_dir} \
#     --output-file ${output_file} \
#     --ifos 'L1' \