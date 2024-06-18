#!/bin/bash

# 指定要搜索的根目录
SEARCH_DIR="/mnt/geogpt-gpfs/llm-course/ossutil_output/public/tianwen/npy/fineweb_edu_sample_100BT"
# 指定输出文件的路径
OUTPUT_FILE="/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training/txt/fineweb_edu_sample_100BT.txt" # 替换为已有的txt文件的路径

# 使用find命令查找所有.npy文件，并格式化输出到文本文件
find "$SEARCH_DIR" -type f -name "*.npy" -print | 
  awk '{print "  - " $0}' >> "$OUTPUT_FILE"

echo "List of .npy files has been appended to $OUTPUT_FILE"