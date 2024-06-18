export OMP_NUM_THREADS=16


python3 -u -m torch.distributed.run \
  --nproc_per_node=8 \
  --log-dir=/mnt/geogpt-gpfs/llm-course/home/zhangjianxing/OLMo/output/logs \
  --tee=3 \
  --standalone \
  /mnt/geogpt-gpfs/llm-course/home/lfu/OLMo/scripts/train.py \
  /mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training/OLMo-2B-stella-a100-jiaminghui.yaml \
  --save-folder=/mnt/geogpt-gpfs/llm-course/home/jiaminghui/output
