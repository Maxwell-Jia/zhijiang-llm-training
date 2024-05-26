#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
OUTPUT_DIR=${INPUT_DIR}/datasets
DATASETS_DIR=/mnt/geogpt-gpfs/llm-course/public/datasets

python ${INPUT_DIR}/src/exp/extract_astronomy_data.py \
    --examples_path ${INPUT_DIR}/datasets/astro-examples.jsonl \
    --documents_dir ${DATASETS_DIR}/wikipedia/20231101.en/ \
    --output_path ${OUTPUT_DIR}/wiki-astro-epoch-3.jsonl \
    --similar_threshold 0.4 \
    --max_items 9999999 \
    --gpu 1 \
    > ${INPUT_DIR}/outputs/astro-wiki-epoch-3.log 2>&1