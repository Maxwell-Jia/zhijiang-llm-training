#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/huggingface/

source /mnt/geogpt-gpfs/llm-course/home/jiaminghui/Miniconda3/bin/activate
conda activate llm

python llama3.py
