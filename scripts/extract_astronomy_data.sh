#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
OUTPUT_DIR=${INPUT_DIR}/datasets
DATASETS_DIR=/mnt/geogpt-gpfs/llm-course/public/datasets

python ${INPUT_DIR}/src/exp/extract_astronomy_data.py \
    --examples_path ${INPUT_DIR}/datasets/astro-wiki-examples.jsonl \
    --documents_dir ${DATASETS_DIR}/wikipedia/20231101.en/ \
    --output_path ${OUTPUT_DIR}/wiki-astro.jsonl \
    --max_items 5 \
    --gpu 7 \
    > ${OUTPUT_DIR}/extract_astro.log 2>&1