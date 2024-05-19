#!/bin/bash

python src/exp/run_pretrain.py \
    --config_name configs/models/Llama-300M.json \
    --tokenizer_name nvidia/Llama3-ChatQA-1.5-8B \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --block_size 8192 \
    --max_train_samples 1000 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --do_train \
    --output_dir ./outputs/debug
