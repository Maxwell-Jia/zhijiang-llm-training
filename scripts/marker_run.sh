export TEXIFY_MODEL_MAX=2000
export NUM_DEVICES=6
export NUM_WORKERS=2
export INFERENCE_RAM=80

marker_chunk_convert \
  /mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/books/pdf-en/11 \
  /mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/books/mmd-en \
  