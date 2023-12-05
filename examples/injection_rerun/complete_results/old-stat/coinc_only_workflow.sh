#!/bin/bash

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

stat=old #old or new

### Findtrigs

# pycbc_coinc_findtrigs \
#     --statistic-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/statHL.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1-multiparam.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/L1-multiparam.hdf \
#     --coinc-threshold 0.002 \
#     --sngl-ranking newsnr_sgveto \
#     --ranking-statistic phasetd_exp_fit_fgbg_norm \
#     --randomize-template-order \
#     --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
#     --template-bank \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1L1-BBHBANK-1235750266-2415776.hdf \
#     --trigger-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/H1_week_1_${stat}_stat_no_inj.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/L1_week_1_${stat}_stat_no_inj.hdf \
#     --pivot-ifo H1 \
#     --fixed-ifo L1 \
#     --output-file \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_1_no_inj.hdf \
#     --nprocesses 15 \
#     --timeslide-interval 0.1 \
#     --verbose

# pycbc_coinc_findtrigs \
#     --statistic-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/statHL.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1-multiparam.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/L1-multiparam.hdf \
#     --coinc-threshold 0.002 \
#     --sngl-ranking newsnr_sgveto \
#     --ranking-statistic phasetd_exp_fit_fgbg_norm \
#     --randomize-template-order \
#     --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
#     --template-bank \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1L1-BBHBANK-1235750266-2415776.hdf \
#     --trigger-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/H1_week_2_${stat}_stat_no_inj.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/L1_week_2_${stat}_stat_no_inj.hdf \
#     --pivot-ifo H1 \
#     --fixed-ifo L1 \
#     --output-file \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_2_no_inj.hdf \
#     --nprocesses 15 \
#     --timeslide-interval 0.1 \
#     --verbose

# ### Findtrigs Inj

# pycbc_coinc_findtrigs \
#     --statistic-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/statHL.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1-multiparam.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/L1-multiparam.hdf \
#     --coinc-threshold 0.002 \
#     --sngl-ranking newsnr_sgveto \
#     --ranking-statistic phasetd_exp_fit_fgbg_norm \
#     --randomize-template-order \
#     --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
#     --template-bank \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1L1-BBHBANK-1235750266-2415776.hdf \
#     --trigger-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/H1_week_1_${stat}_stat_with_inj.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/L1_week_1_${stat}_stat_with_inj.hdf \
#     --pivot-ifo H1 \
#     --fixed-ifo L1 \
#     --output-file \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_1_with_inj.hdf \
#     --nprocesses 15 \
#     --verbose

# pycbc_coinc_findtrigs \
#     --statistic-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/statHL.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1-multiparam.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/L1-multiparam.hdf \
#     --coinc-threshold 0.002 \
#     --sngl-ranking newsnr_sgveto \
#     --ranking-statistic phasetd_exp_fit_fgbg_norm \
#     --randomize-template-order \
#     --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
#     --template-bank \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/H1L1-BBHBANK-1235750266-2415776.hdf \
#     --trigger-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/H1_week_2_${stat}_stat_with_inj.hdf \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/L1_week_2_${stat}_stat_with_inj.hdf \
#     --pivot-ifo H1 \
#     --fixed-ifo L1 \
#     --output-file \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_2_with_inj.hdf \
#     --nprocesses 15 \
#     --verbose

# ### Coinc Statmap

# pycbc_coinc_statmap \
#     --max-hierarchical-removal 15 \
#     --hierarchical-removal-against exclusive \
#     --veto-window 0.1 \
#     --cluster-window 10.0 \
#     --limit-ifar H1:1000 L1:1000 \
#     --coinc-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_1_no_inj.hdf \
#     --ifos L1 H1 \
#     --output-file \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_week_1_no_inj.hdf \
#     --verbose

# pycbc_coinc_statmap \
#     --max-hierarchical-removal 15 \
#     --hierarchical-removal-against exclusive \
#     --veto-window 0.1 \
#     --cluster-window 10.0 \
#     --limit-ifar H1:1000 L1:1000 \
#     --coinc-files \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_2_no_inj.hdf \
#     --ifos L1 H1 \
#     --output-file \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_week_2_no_inj.hdf \
#     --verbose

# ### Coinc Statmap Inj

# pycbc_coinc_statmap_inj \
#     --veto-window 0.1 \
#     --cluster-window 10.0 \
#     --limit-ifar H1:1000 L1:1000 \
#     --zero-lag-coincs \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_1_with_inj.hdf \
#     --full-data-background \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_week_1_no_inj.hdf \
#     --ifos L1 H1 \
#     --output-file \
#             /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_INJ_week_1_with_inj.hdf \
#     --verbose

# pycbc_coinc_statmap_inj \
#     --veto-window 0.1 \
#     --cluster-window 10.0 \
#     --limit-ifar H1:1000 L1:1000 \
#     --zero-lag-coincs \
#       /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-COINC_week_2_with_inj.hdf \
#     --full-data-background \
#        /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_week_2_no_inj.hdf \
#     --ifos L1 H1 \
#     --output-file \
#             /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_INJ_week_2_with_inj.hdf \
#     --verbose

### HDF inj find

pycbc_coinc_hdfinjfind \
    --trigger-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_INJ_week_1_with_inj.hdf \
    --injection-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/injection-frames/bbh_injs-1262192988-1263751886.xml \
    --injection-window 2.0 \
    --output-file \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-HDFINJFIND_week_1.hdf \
    --verbose

pycbc_coinc_hdfinjfind \
    --trigger-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-STATMAP_INJ_week_2_with_inj.hdf \
    --injection-files \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/injection-frames/bbh_injs-1262192988-1263751886.xml \
    --injection-window 2.0 \
    --output-file \
      /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/complete_results/${stat}-stat/H1L1-HDFINJFIND_week_2.hdf \
    --verbose
