# 设置环境变量
export CUDA_VISIBLE_DEVICES=7

nougat \
  /mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/books/pdf-en/1/1-2 \
  -o /mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/books/mmd-en \
  -b 8 \
  -c /mnt/geogpt-gpfs/llm-course/home/zhangjianxing/nougat/0.1.0-base \
  --no-skipping