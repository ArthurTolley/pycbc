#!/bin/bash

set -e

# Pre-requisites:
# - Merger trigger files

# Workflow:
# - Coinc findtrigs - H1L1
# - Coinc findtrigs inj - H1L1
#
# - Coinc statmap - H1L1
#
# - Coinc statmap inj - H1L1
#
# - Add Statmap - Inj & No Inj
#
# - hdfinjfind

## Collate Triggers
output_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/trigger-merges/'
trigger_file_list=/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/trigger-merges/new_stat_no_injs.txt

output_file=H1_new_stat_no_injs.hdf
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
    --trigger-file-list ${trigger_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'H1' \

output_file=L1_new_stat_no_injs.hdf
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
    --trigger-file-list ${trigger_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'L1' \

trigger_file_list=/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/trigger-merges/new_stat_with_injs.txt

output_file=H1_new_stat_with_injs.hdf
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
    --trigger-file-list ${trigger_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'H1' \

output_file=L1_new_stat_with_injs.hdf
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
    --trigger-file-list ${trigger_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'L1' \

## Findtrigs

pycbc_coinc_findtrigs \
    --statistic-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/statHL.hdf \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/H1-OLD_STAT_multiparam.hdf \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/L1-OLD_STAT_multiparam.hdf \
    --coinc-threshold 0.002 \
    --sngl-ranking newsnr_sgveto \
    --ranking-statistic phasetd_exp_fit_fgbg_norm \
    --randomize-template-order \
    --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
    --template-bank \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/run-files/H1L1-BBHBANK-1235750266-2415776.hdf \
    --trigger-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/trigger-merges/H1_new_stat_no_injs.hdf \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/trigger-merges/L1_new_stat_no_injs.hdf \
    --pivot-ifo H1 \
    --fixed-ifo L1 \
    --output-file \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/findtrigs/H1L1-COINC_no_injs.hdf \
    --nprocesses 15 \
    --timeslide-interval 0.1 \
    --verbose

### Findtrigs Inj

pycbc_coinc_findtrigs \
    --statistic-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/statHL.hdf \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/H1-OLD_STAT_multiparam.hdf \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/L1-OLD_STAT_multiparam.hdf \
    --coinc-threshold 0.002 \
    --sngl-ranking newsnr_sgveto \
    --ranking-statistic phasetd_exp_fit_fgbg_norm \
    --randomize-template-order \
    --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
    --template-bank \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/run-files/H1L1-BBHBANK-1235750266-2415776.hdf \
    --trigger-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/trigger-merges/H1_new_stat_with_injs.hdf \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/trigger-merges/L1_new_stat_with_injs.hdf \
    --pivot-ifo H1 \
    --fixed-ifo L1 \
    --output-file \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/findtrigs/H1L1-COINC_with_injs.hdf \
    --nprocesses 15 \
    --verbose

### Coinc Statmap

pycbc_coinc_statmap \
    --max-hierarchical-removal 15 \
    --hierarchical-removal-against exclusive \
    --veto-window 0.1 \
    --cluster-window 10.0 \
    --limit-ifar H1:1000 L1:1000 \
    --coinc-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/findtrigs/H1L1-COINC_no_injs.hdf \
    --ifos L1 H1 \
    --output-file \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/statmap/H1L1-STATMAP_no_injs.hdf \
    --verbose

### Coinc Statmap Inj

pycbc_coinc_statmap_inj \
    --veto-window 0.1 \
    --cluster-window 10.0 \
    --limit-ifar H1:1000 L1:1000 \
    --zero-lag-coincs \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/findtrigs/H1L1-COINC_with_injs.hdf \
    --full-data-background \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/statmap/H1L1-STATMAP_no_injs.hdf \
    --ifos L1 H1 \
    --output-file \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/statmap/H1L1-STATMAP_INJ_with_injs.hdf \
    --verbose

### HDF inj find

pycbc_coinc_hdfinjfind \
    --trigger-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/statmap/H1L1-STATMAP_INJ_with_injs.hdf \
    --injection-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/injection-frames/bbh_injs-1262192988-1263751886.xml \
    --injection-window 2.0 \
    --output-file \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/fits-only/hdfinjfind/H1L1-HDFINJFIND_BBH_RATESINJ_INJECTIONS-1262995020-600000.hdf \
    --verbose
