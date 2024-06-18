dolma tokens \
    --destination "/mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/fineweb-edu-sample-100BT/npy_data/7/"   \
    --documents "/mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/fineweb-edu-sample-100BT/documents/7/part_*.jsonl.gz" \
    --tokenizer.name_or_path "EleutherAI/gpt-neox-20b" \
    --tokenizer.eos_token_id 0 \
    --tokenizer.pad_token_id 0 \
    --processes 15