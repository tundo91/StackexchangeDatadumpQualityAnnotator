#!/usr/bin/env bash

# activate local virtualenv
source venv/bin/activate &&

# ETL from DB to local JSON files
#python manage.py ETL_stack_threads &&
#python manage.py ETL_stack_cooccurrence_network &&
#python manage.py ETL_stack_ARN_network &&
#python manage.py ETL_stack_ABAN_network &&
#python manage.py ETL_stack_CBEN_network &&
#python manage.py ETL_stack_users &&

N_PARTITIONS=4
DB='travel'
TASK_NAME='binaryBestAnswer'
SRC_FILE_NAME='threads_all_shared.json'

python -m Analysis.feats_extract --n_partitions ${N_PARTITIONS} --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.AA_dataset_builder