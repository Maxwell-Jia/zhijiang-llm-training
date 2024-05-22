#!/bin/bash

# Set environment variables
export INPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training
export OUTPUT_DIR=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/output

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

# Install dependencies
pip install -r ${INPUT_DIR}/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# Run the pretraining script with specified parameters
python ${INPUT_DIR}/src/exp/run_pretrain.py \
    --config_name ${INPUT_DIR}/configs/models/Llama-2-300M.json \
    --tokenizer_name TinyPixel/Llama-2-7B-bf16-sharded \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --block_size 1024 \
    --per_device_train_batch_size 64 \
    --per_device_eval_batch_size 64 \
    --do_train \
    --output_dir ${OUTPUT_DIR}/llama-2-300m_wikitext \
    --max_steps 1000 \
    --warmup_steps 50 \
    --logging_steps 100 \
    --save_steps 2500 \
    --seed 2024 \
    --bf16 true \
    --learning_rate 2e-4 \
    --report_to tensorboard \
    > ${OUTPUT_DIR}/llama-2-300m_wikitext.log 2>&1
