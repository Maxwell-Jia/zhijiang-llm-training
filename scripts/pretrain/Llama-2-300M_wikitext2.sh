#!/bin/bash

export CUDA_VISIBLE_DEVICES=7

python src/exp/run_pretrain.py \
    --config_name configs/models/Llama-2-300M.json \
    --tokenizer_name TinyPixel/Llama-2-7B-bf16-sharded \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --block_size 1024 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --do_train \
    --output_dir ./outputs/llama-2-300m_wikitext \
    --max_steps 1000 \
    --warmup_steps 50 \
    --logging_steps 100 \
    --save_steps 2500 \
    --seed 2024 \
    --bf16 true \
    --learning_rate 1e-4 \
