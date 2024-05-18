from datasets import load_dataset
import argparse

parser = argparse.ArgumentParser(description='Download dataset')
parser.add_argument('--dataset', type=str, default='imdb', help='dataset name')
parser.add_argument('--cache_dir', type=str, default='/mnt/geogpt-gpfs/llm-course/home/jiaminghui/datasets', help='cache directory')
args = parser.parse_args()

# Download dataset
dataset = load_dataset(args.dataset, cache_dir=args.cache_dir)