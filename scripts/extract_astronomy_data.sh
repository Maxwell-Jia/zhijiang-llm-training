#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
OUTPUT_DIR=${INPUT_DIR}/datasets
DATASETS_DIR=/mnt/geogpt-gpfs/llm-course/public/datasets

python ${INPUT_DIR}/src/exp/extract_astronomy_data.py \
    --astro_title_path ${INPUT_DIR}/datasets/astro-title.txt \
    --document_dir ${DATASETS_DIR}/dolma_v1_7/CC_head/documents \
    --similar_threshold 0.8 \
    --output_path ${OUTPUT_DIR}/astro_text.jsonl \
    --max_items 1000