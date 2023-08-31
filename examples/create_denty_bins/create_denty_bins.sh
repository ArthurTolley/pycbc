#!/bin/bash

# pycbc_fit_sngls_by_template \
#   --fit-function exponential  \
#   --stat-threshold 6.0 \
#   --prune-param mtotal \
#   --log-prune-param  \
#   --prune-bins 2 \
#   --prune-number 2 \
#   --sngl-ranking newsnr_sgveto \
#   --ifo L1 \
#   --trigger-file /home/arthur.tolley/PyCBC_changes/live_stat/trigger_files/test/2023_06_20.hdf \
#   --bank-file /home/arthur.tolley/PyCBC_changes/live_stat/pycbc/examples/live/O4_DESIGN_OPT_FLOW_HYBRID_BANK_O3_CONFIG.hdf \
#   --output L1-test-coeffs.hdf \
#   --verbose

#--veto-file H1L1V1-VETOES-1186740100-3400.xml \
#--veto-segment-name vetoes \

# pycbc_fit_sngls_over_param \
#   --verbose \
#   --template-fit-file L1-test-coeffs.hdf \
#   --bank-file /home/arthur.tolley/PyCBC_changes/live_stat/pycbc/examples/live/O4_DESIGN_OPT_FLOW_HYBRID_BANK_O3_CONFIG.hdf \
#   --output L1-test.hdf \
#   --fit-param template_duration \
#   --log-param \
#   --regression-method tricube \
#   --smoothing-width 0.4 \
#   --f-lower 15.0

pycbc_fit_sngls_over_multiparam \
  --verbose \
  --template-fit-file L1-test-coeffs.hdf \
  --bank-file /home/arthur.tolley/PyCBC_changes/live_stat/pycbc/examples/live/O4_DESIGN_OPT_FLOW_HYBRID_BANK_O3_CONFIG.hdf \
  --output L1-multiparam.hdf \
  --fit-param template_duration chi_eff eta \
  --f-lower 15.0 \
  --log-param True False False \
  --smoothing-width 0.4 0.2 0.08 \
