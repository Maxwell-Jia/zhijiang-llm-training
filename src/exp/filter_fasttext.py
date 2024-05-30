import os
from sentence_transformers import SentenceTransformer
import gzip
import json
import torch
import argparse
import time
from tqdm import tqdm
import pyarrow.parquet as pq


def main(args):
    device = torch.device("cpu" if args.gpu == None else f"cuda:{args.gpu}")

    # Load sentence embeddings model
    model = SentenceTransformer(args.model_name, device=device, cache_folder=args.cache_dir)

    # Load astronomy examples text from wikipedia and megawiki
    examples = []
    with open(args.examples_path, "r") as f:
        for line in f:
            data = json.loads(line)
            examples.append(data["text"])
    
    # Embedding examples text
    example_embeddings = model.encode(
        examples,
        show_progress_bar=True,
        batch_size=args.batch_size,
        convert_to_numpy=False,
        normalize_embeddings=True,
        device=device,
    )
    example_embeddings = torch.vstack(example_embeddings)

    # Load documents text
    with open(args.jsonl_path, "r") as f:
        json_lines = [json.loads(line) for line in f]
    
    item_count = 0
    for i in tqdm(range(0, len(json_lines), args.batch_size)):
        batch = json_lines[i:i+args.batch_size]
        documents = [data["text"] for data in batch]
        
        # Embedding documents text
        docs_embeddings = model.encode(
            documents,
            show_progress_bar=False,
            batch_size=args.batch_size,
            convert_to_numpy=False,
            normalize_embeddings=True,
            device=device,
        )
        docs_embeddings = torch.vstack(docs_embeddings)

        # Calculate the similarity matrix of astronomy titles and dolma titles.
        # Columns of the matrix represents dolma titles, and the rows represent astronomy titles.
        title_similar_matrix = torch.matmul(example_embeddings, docs_embeddings.T)
        max_similar = title_similar_matrix.max(dim=0).values

        idx_over_threshold = torch.where(max_similar >= args.similar_threshold)[0].cpu().numpy()

        # Save to jsonl file
        with open(args.output_path, "a") as f:
            for idx in idx_over_threshold:
                f.write(json.dumps(batch[idx]) + "\n")

        item_count += idx_over_threshold.shape[0]

    print(f"Saved {item_count} items to {args.output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--examples_path",
        default=None,
        type=str,
        required=True,
        help="A small amount of sample text. You can generate it by gpt4. The file should be a jsonl file."
    )
    parser.add_argument(
        "--jsonl_path",
        default=None,
        type=str,
        required=True,
        help="The path of the documents you want to search text which is similar with the sample text."
    )
    parser.add_argument(
        "--output_path",
        default=None,
        type=str,
        required=True,
        help="The output path of the jsonl file.",
    )
    parser.add_argument(
        "--batch_size",
        default=8192,
        type=int,
        help="The batch size for computing semetic similarity.",
    )
    parser.add_argument(
        "--similar_threshold",
        default=0.8,
        type=float,
        help="The threshold of the similarity between the sample text and the document text.",
    )
    parser.add_argument(
        "--gpu",
        default=None,
        type=int,
        help="The GPU ID you want to use.",
    )
    parser.add_argument(
        "--model_name",
        default="flax-sentence-embeddings/all_datasets_v4_MiniLM-L6",
        type=str,
        help="The embedding model name you want to use.",
    )
    parser.add_argument(
        "--cache_dir",
        default="./pretrained",
        type=str,
        help="The directory to store the pretrained models.",
    )
    args = parser.parse_args()

    main(args)