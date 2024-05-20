#!/bin/bash

export CUDA_VISIBLE_DEVICES=7

python src/exp/run_pretrain.py \
    --config_name configs/models/Llama-300M.json \
    --tokenizer_name TinyPixel/Llama-2-7B-bf16-sharded \
    --dataset_name devingulliver/dolma-v1_6-sample \
    --block_size 1024 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --do_train \
    --output_dir ./outputs/llama-300m-dolma-sample \
    --max_steps 1000 \
    --warmup_steps 50 \
    --logging_steps 100 \
    --save_steps 2500 \
    --seed 2024 \
    --bf16 \
    --torch_compile \
    --learning_rate 1e-4 \
