#!/bin/bash

INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
OUTPUT_DIR=${INPUT_DIR}/datasets
DATASETS_DIR=/mnt/geogpt-gpfs/llm-course/public/datasets

python -u ${INPUT_DIR}/src/exp/extract_astro_data_fasttext.py \
    --model_path ${INPUT_DIR}/outputs/astro-or-not-classifier/model.bin \
    --data_dir ${DATASETS_DIR}/dolma_v1_7/C4/documents \
    --output_path ${INPUT_DIR}/datasets/astro-c4-fasttext.jsonl \
    --threshold 0.95 \
    --skip_files 49 \
    > ${INPUT_DIR}/outputs/astro-c4-fasttext.log 2>&1