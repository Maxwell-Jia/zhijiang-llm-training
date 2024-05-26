#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
OUTPUT_DIR=${INPUT_DIR}/datasets
DATASETS_DIR=/mnt/geogpt-gpfs/llm-course/public/datasets

python ${INPUT_DIR}/src/exp/extract_astronomy_data.py \
    --examples_path ${INPUT_DIR}/datasets/astro-examples.jsonl \
    --documents_dir ${DATASETS_DIR}/dolma_v1_7/CC_middle/documents \
    --output_path ${OUTPUT_DIR}/cc_middle-astro-epoch-3.jsonl \
    --similar_threshold 0.4 \
    --max_items 9999999 \
    --gpu 4 \
    --batch_size 4096 \
    > ${INPUT_DIR}/outputs/cc_middle-astro-epoch-3.log 2>&1