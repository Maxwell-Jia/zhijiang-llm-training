#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
OUTPUT_DIR=${INPUT_DIR}/datasets
DATASETS_DIR=/mnt/geogpt-gpfs/llm-course/public/datasets

python ${INPUT_DIR}/src/exp/extract_astronomy_data.py \
    --examples_path ${INPUT_DIR}/datasets/astro-wiki-examples.jsonl \
    --documents_dir ${DATASETS_DIR}/dolma_v1_7/C4/documents \
    --output_path ${OUTPUT_DIR}/c4-astro.jsonl \
    --max_items 9999999 \
    --gpu 6 \
    > ${INPUT_DIR}/c4-astro.log 2>&1