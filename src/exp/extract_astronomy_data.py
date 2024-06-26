"""
Script for extracting documents similar to astronomy or physics titles using sentence embeddings.

This script takes astronomy or physics titles generated by GPT-4, and a directory containing JSON files of documents.
It calculates the similarity between the titles and document titles using a pre-trained sentence embeddings model.
Documents with a similarity score above a specified threshold are saved to a JSONL file.
"""

import os
from sentence_transformers import SentenceTransformer
import gzip
import json
import torch
import argparse
import time
from tqdm import tqdm
import pyarrow.parquet as pq


def load_file(file_path):
    id_list, text_list = [], []

    if file_path.endswith(".json.gz"):
        with gzip.open(file_path, "rt") as f:
            for line in f:
                data = json.loads(line)
                id_list.append(data["id"])
                text_list.append(data["text"])
    
    elif file_path.endswith(".json") or file_path.endswith(".jsonl"):
        with open(file_path, "r") as f:
            for line in f:
                data = json.loads(line)
                id_list.append(data["id"])
                text_list.append(data["text"])

    elif file_path.endswith(".parquet"):
        table = pq.read_table(file_path).to_pandas()
        id_list = table["id"].tolist()
        text_list = table["text"].tolist()
    
    else:
        raise ValueError("Unknown file format.")
    
    return id_list, text_list


def main(args):
    device = torch.device("cpu" if args.gpu == None else f"cuda:{args.gpu}")

    # Load sentence embeddings model
    model = SentenceTransformer(args.model_name, device=device, cache_folder=args.cache_dir)

    # Load astronomy or physics titles generated by gpt4
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

    # Get documents
    docs_list = os.listdir(args.documents_dir)
    tmp = [item for item in docs_list if not item.endswith(".swp")]
    docs_list = tmp
    if len(docs_list) == 0:
        raise ValueError("No documents found in the directory.")
    docs_list.sort()

    item_count = 0
    for docs in docs_list:
        # Load .json.gz file
        print(f"Loading file: {docs}")
        docs = os.path.join(args.documents_dir, docs)
        start_time = time.time()
        id_list, text_list = load_file(docs)
        print("File Loaded.")

        # Embedding document titles
        docs_embeddings = model.encode(
            text_list,
            show_progress_bar=True,
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
                f.write(
                    json.dumps(
                        {
                            "id": id_list[idx],
                            "source": docs,
                            "text": text_list[idx],
                        }
                    )
                    + "\n"
                )
        item_count += idx_over_threshold.shape[0]
        print(f"Load {idx_over_threshold.shape[0]} items from {docs}. Current totle: {item_count}")
        end_time = time.time()
        print(f"Time cost: {end_time - start_time} seconds for {docs}")
        
        if item_count >= args.max_items:
            print("Maximum number of items reached.")
            break

    if item_count < args.max_items:
        print(f"Only {item_count} items were extracted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--examples_path",
        default=None,
        type=str,
        required=True,
        help="A small amount of sample text. You can generate it by gpt4. The file should be a jsonl file."
    )
    parser.add_argument(
        "--documents_dir",
        default=None,
        type=str,
        required=True,
        help="The directory containing the documents you want to search text which is similar with the sample text."
    )
    parser.add_argument(
        "--match_col",
        default="text",
        type=str,
        help="The column name of the documents you want to match with the sample text.",
    )
    parser.add_argument(
        "--output_path",
        default=None,
        type=str,
        required=True,
        help="The output path of the jsonl file.",
    )
    parser.add_argument(
        "--max_items",
        default=5,
        type=int,
        help="The maximum number of items you want to extract.",
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
        "--batch_size",
        default=1024,
        type=int,
        help="The batch size for the embedding model.",
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
