#!/bin/bash

gps_start_time=1367939000
gps_end_time=1367939180
f_min=18

./check_results.py \
    --gps-start ${gps_start_time} \
    --gps-end ${gps_end_time} \
    --f-min ${f_min} \
    --bank template_bank.hdf \
    --injections injections.hdf \
    --detectors H1 L1 V1