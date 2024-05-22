#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

RUN_NAME=llama-300m-dolma-sample
INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
OUTPUT_DIR=${INPUT_DIR}/outputs

python ${INPUT_DIR}/src/exp/run_pretrain.py \
    --config_name ${INPUT_DIR}/configs/models/Llama-2-300M.json \
    --tokenizer_name TinyPixel/Llama-2-7B-bf16-sharded \
    --dataset_name devingulliver/dolma-v1_6-sample \
    --block_size 1024 \
    --per_device_train_batch_size 32 \
    --do_train \
    --output_dir ${OUTPUT_DIR}/${RUN_NAME} \
    --max_steps 1000 \
    --warmup_steps 50 \
    --logging_steps 100 \
    --save_steps 2500 \
    --seed 2024 \
    --bf16 \
    --torch_compile \
    --learning_rate 2e-4 \
    # > ${OUTPUT_DIR}/${RUN_NAME}.log 2>&1
