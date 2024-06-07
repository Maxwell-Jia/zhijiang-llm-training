import gzip
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def write_chunk(lines, output_file):
    with gzip.open(output_file, 'wt', encoding='utf-8') as outfile:
        outfile.writelines(lines)
    print(f'Saving {output_file}')

def split_jsonl_gz(input_file, output_dir, lines_per_file, num_threads=4):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with gzip.open(input_file, 'rt', encoding='utf-8') as infile:
        file_index = 0
        lines = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for line_index, line in tqdm(enumerate(infile)):
                lines.append(line)
                if (line_index + 1) % lines_per_file == 0:
                    output_file = os.path.join(output_dir, f'part_{file_index:03d}.jsonl.gz')
                    executor.submit(write_chunk, lines, output_file)
                    file_index += 1
                    lines = []
            # Handle any remaining lines
            if lines:
                output_file = os.path.join(output_dir, f'part_{file_index:03d}.jsonl.gz')
                executor.submit(write_chunk, lines, output_file)


# 使用示例
input_file = '/mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/fineweb-edu-sample-100BT/documents/00000.jsonl.gz'
output_dir = '/mnt/geogpt-gpfs/llm-course/public/tianwen/datasets/fineweb-edu-sample-100BT/documents/'
# 9700w / 200 = 500000
lines_per_file = 500_000
num_threads =  8

split_jsonl_gz(input_file, output_dir, lines_per_file, num_threads)
