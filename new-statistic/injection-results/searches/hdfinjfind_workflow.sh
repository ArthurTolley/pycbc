#!/bin/bash

# Pre-requisites:
# - Create folders
# - Merger trigger files

# Workflow:
# - Coinc findtrigs - H1L1
# - Coinc findtrigs Inj - H1L1
# - Coinc statmap - H1L1
# - Coinc statmap Inj - H1L1
# - Add Statmap - Inj & No Inj
# - hdfinjfind

set -e

# ----------------------
# Set constant variables
stat_file='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/statHL.hdf'
H1_fit_file='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/H1-OLD_STAT_multiparam.hdf'
L1_fit_file='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/statistic-files/L1-OLD_STAT_multiparam.hdf'
template_bank='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/run-files/H1L1-BBHBANK-1235750266-2415776.hdf'
inj_file='home/arthur.tolley/PyCBC_changes/temp_fit_infra/injection-frames/bbh_injs-1262192988-1263751886.xml'

# ------------------------------
# Set search dependent variables

# Old Stat
statistic='old-stat'
sngl_ranking='newsnr_sgveto'
ranking_statistic='phasetd'
no_inj_search_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_no_injs'
w_inj_search_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_with_injs'

# Fits + PSD Var
# statistic='fits-psd-var'
# sngl_ranking='newsnr_sgveto_psdvar_threshold'
# ranking_statistic='phasetd_exp_fit_fgbg_norm'
# no_inj_search_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/week-2/new-stat/no-injs'
# w_inj_search_dir='/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/week-2/new-stat/with-injs'

# --------------------------
# Create directory structure
directory="./${statistic}"

if [ ! -d "$directory" ]; then
    echo "Creating ${statistic} directory."
    mkdir -p "${directory}"
    mkdir -p "${directory}/findtrigs"
    mkdir -p "${directory}/statmap"
    mkdir -p "${directory}/hdfinjfind"
    mkdir -p "${directory}/trigger-merges"
    echo "${statistic} directory created successfully."
else
  echo "${statistic} directory already exists."
  if [ ! -d "$directory/findtrigs" ]; then
    echo " Creating findtrigs subdirectory"
    mkdir -p "${directory}/findtrigs"
  fi
  if [ ! -d "$directory/statmap" ]; then
    echo " Creating statmap subdirectory"
    mkdir -p "${directory}/statmap"
  fi
  if [ ! -d "$directory/hdfinjfind" ]; then
    echo " Creating hdfinjfind subdirectory"
    mkdir -p "${directory}/hdfinjfind"
  fi
  if [ ! -d "$directory/trigger-merges" ]; then
    echo " Creating trigger-merges subdirectory"
    mkdir -p "${directory}/trigger-merges"
  fi
fi

# -------------------------------------------
# Get the list of trigger files from a search
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/new-statistic/injection-results/get_search_trigger_files.py \
    --stat ${statistic} \
    --no-inj-search-dir ${no_inj_search_dir} \
    --with-inj-search-dir ${w_inj_search_dir} \
    --output-location ${directory}

no_inj_trig_file_list="${directory}/${statistic}_no_injs.txt"
with_inj_trig_file_list="${directory}/${statistic}_with_injs.txt"

# ----------------------------------
# Collate Triggers into one hdf file
output_dir="${directory}/trigger-merges/"

output_file=H1_no_injs.hdf
# python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
#     --trigger-file-list ${no_inj_trig_file_list} \
#     --output-dir ${output_dir} \
#     --output-file ${output_file} \
#     --ifos 'H1' \

output_file=L1_no_injs.hdf
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
    --trigger-file-list ${no_inj_trig_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'L1' \


output_file=H1_with_injs.hdf
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
    --trigger-file-list ${with_inj_trig_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'H1' \

output_file=L1_with_injs.hdf
python /home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/template_fits/collate_live_triggers.py \
    --trigger-file-list ${with_inj_trig_file_list} \
    --output-dir ${output_dir} \
    --output-file ${output_file} \
    --ifos 'L1' \

# ---------
# Findtrigs
pycbc_coinc_findtrigs \
    --statistic-files \
      ${stat_file} \
      ${H1_fit_file} \
      ${L1_fit_file} \
    --coinc-threshold 0.002 \
    --sngl-ranking ${sngl_ranking} \
    --ranking-statistic ${ranking_statistic} \
    --randomize-template-order \
    --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
    --template-bank \
      ${template_bank} \
    --trigger-files \
      ${directory}/trigger-merges/H1_no_injs.hdf \
      ${directory}/trigger-merges/L1_no_injs.hdf \
    --pivot-ifo H1 \
    --fixed-ifo L1 \
    --output-file \
      ${directory}/findtrigs/H1L1-COINC_no_injs.hdf \
    --nprocesses 15 \
    --timeslide-interval 0.1 \
    --verbose

# -------------
# Findtrigs Inj
pycbc_coinc_findtrigs \
    --statistic-files \
      ${stat_file} \
      ${H1_fit_file} \
      ${L1_fit_file} \
    --coinc-threshold 0.002 \
    --sngl-ranking ${sngl_ranking} \
    --ranking-statistic ${ranking_statistic} \
    --randomize-template-order \
    --loudest-keep-values [20:10,15:5,10:30,5:30,0:30] \
    --template-bank \
      ${template_bank} \
    --trigger-files \
      ${directory}/trigger-merges/H1_with_injs.hdf \
      ${directory}/trigger-merges/L1_with_injs.hdf \
    --pivot-ifo H1 \
    --fixed-ifo L1 \
    --output-file \
      ${directory}/findtrigs/H1L1-COINC_with_injs.hdf \
    --nprocesses 15 \
    --verbose

# -------------
# Coinc Statmap
pycbc_coinc_statmap \
    --max-hierarchical-removal 15 \
    --hierarchical-removal-against exclusive \
    --veto-window 0.1 \
    --cluster-window 10.0 \
    --limit-ifar H1:1000 L1:1000 \
    --coinc-files \
      ${directory}/findtrigs/H1L1-COINC_no_injs.hdf \
    --ifos L1 H1 \
    --output-file \
      ${directory}/statmap/H1L1-STATMAP_no_injs.hdf \
    --verbose

# -----------------
# Coinc Statmap Inj
pycbc_coinc_statmap_inj \
    --veto-window 0.1 \
    --cluster-window 10.0 \
    --limit-ifar H1:1000 L1:1000 \
    --zero-lag-coincs \
      ${directory}/findtrigs/H1L1-COINC_with_injs.hdf \
    --full-data-background \
      ${directory}/statmap/H1L1-STATMAP_no_injs.hdf \
    --ifos L1 H1 \
    --output-file \
      ${directory}statmap/H1L1-STATMAP_INJ_with_injs.hdf \
    --verbose

# ------------
# HDF inj find
pycbc_coinc_hdfinjfind \
    --trigger-files \
     ${directory}/statmap/H1L1-STATMAP_INJ_with_injs.hdf \
    --injection-files \
      ${inj_file} \
    --injection-window 2.0 \
    --output-file \
      ${directory}/hdfinjfind/H1L1-HDFINJFIND_BBH_RATESINJ_INJECTIONS-1262995020-600000.hdf \
    --verbose
