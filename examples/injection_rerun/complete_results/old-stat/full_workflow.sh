#!/bin/bash

# Pre-requisites:
# - Merger trigger files

# Workflow:
# - Single findtrigs - H1 & L1
# - Single findtrigs inj - H1 & L1
# - Coinc findtrigs - H1L1
# - Coinc findtrigs inj - H1L1
#
# - Singles statmaps - H1 & L1
# - Coinc statmap - H1L1
#
# - Exclude Zerolags - H1 & L1 & H1L1
#
# - Singles statmaps inj - H1 & L1
# - Coinc statmap inj - H1L1
#
# - Add Statmap - Inj & No Inj
#
# - hdfinjfind

stat=old #old or new
inj_state=no #no or with

### H1

pycbc_sngls_findtrigs \
    --statistic-files statHL.hdf H1-multiparam.hdf L1-multiparam.hdf \
    --trigger-cuts \
      newsnr_sgveto:9:lower \
      traditional_chisq:2:upper \
    --template-cuts \
      template_duration:7:lower \
    --sngl-ranking newsnr_sgveto \
    --ranking-statistic phasetd_exp_fit_fgbg_norm \
    --randomize-template-order \
    --template-bank H1L1-BBHBANK-1235750266-2415776.hdf \
    --trigger-files /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/H1_week_1_${stat}_stat_${inj_state}_inj.hdf \
    --output-file /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/sngls_find_trigs/H1-SNGL_week_1_${stat}_${inj_state}.hdf \
    --verbose

pycbc_sngls_findtrigs \
    --statistic-files statHL.hdf H1-multiparam.hdf L1-multiparam.hdf \
    --trigger-cuts \
      newsnr_sgveto:9:lower \
      traditional_chisq:2:upper \
    --template-cuts \
      template_duration:7:lower \
    --sngl-ranking newsnr_sgveto \
    --ranking-statistic phasetd_exp_fit_fgbg_norm \
    --randomize-template-order \
    --template-bank H1L1-BBHBANK-1235750266-2415776.hdf \
    --trigger-files /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/H1_week_2_${stat}_stat_${inj_state}_inj.hdf \
    --output-file /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/sngls_find_trigs/H1-SNGL_week_2_${stat}_${inj_state}.hdf \
    --verbose

### L1

pycbc_sngls_findtrigs \
    --statistic-files statHL.hdf H1-multiparam.hdf L1-multiparam.hdf \
    --trigger-cuts \
      newsnr_sgveto:9:lower \
      traditional_chisq:2:upper \
    --template-cuts \
      template_duration:7:lower \
    --sngl-ranking newsnr_sgveto \
    --ranking-statistic phasetd_exp_fit_fgbg_norm \
    --randomize-template-order \
    --template-bank H1L1-BBHBANK-1235750266-2415776.hdf \
    --trigger-files /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/L1_week_2_${stat}_stat_${inj_state}_inj.hdf \
    --output-file /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/sngls_find_trigs/L1-SNGL_week_2_${stat}_${inj_state}.hdf \
    --verbose

pycbc_sngls_findtrigs \
    --statistic-files statHL.hdf H1-multiparam.hdf L1-multiparam.hdf \
    --trigger-cuts \
      newsnr_sgveto:9:lower \
      traditional_chisq:2:upper \
    --template-cuts \
      template_duration:7:lower \
    --sngl-ranking newsnr_sgveto \
    --ranking-statistic phasetd_exp_fit_fgbg_norm \
    --randomize-template-order \
    --template-bank H1L1-BBHBANK-1235750266-2415776.hdf \
    --trigger-files /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/trigger_merges/L1_week_2_${stat}_stat_${inj_state}_inj.hdf \
    --output-file /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/sngls_find_trigs/L1-SNGL_week_2_${stat}_${inj_state}.hdf \
    --verbose