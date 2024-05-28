import fasttext
import os
import gzip
import json
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
    
    # fast text donot support '\n'
    text_list = [text.replace("\n", " ") for text in text_list]
    
    return id_list, text_list


def main(args):
    model = fasttext.load_model(args.model_path)

    # Load data
    file_list = os.listdir(args.data_dir)
    tmp = [item for item in file_list if not item.endswith(".swp")]
    file_list = tmp
    if len(file_list) == 0:
        raise ValueError("No files found in the data directory.")
    file_list.sort()
    file_list = file_list[args.skip_files:]

    item_count = 0
    for file in file_list:
        start = time.time()
        print(f"Loading file: {file}")
        file_path = os.path.join(args.data_dir, file)
        id_list, text_list = load_file(file_path)
        # fast text donot support '\n'
        text_list_replaced = [text.replace("\n", " ") for text in text_list]
        print(f"Loaded {len(id_list)} examples.")
        load_time = time.time() - start
        print(f"Loaded in {load_time} seconds.")

        # Predict
        predictions = model.predict(text_list_replaced)
        astro_text_idx = [i for i, pred in enumerate(predictions[0]) \
                          if pred[0] == "__label__astronomy" \
                            and predictions[1][i] >= args.threshold]
        pred_time = time.time() - start - load_time
        print(f"Predicted in {pred_time} seconds.")
        print(f"Found {len(astro_text_idx)} astro examples.")
        
        # Save predictions
        with open(args.output_path, 'a') as f:
            for i in astro_text_idx:
                f.write(json.dumps({
                    "source": file_path,
                    "id": id_list[i],
                    "text": text_list[i],
                }) + '\n')
        
        item_count += len(astro_text_idx)
        if item_count >= args.max_items:
            break
    
    if item_count < args.max_items:
        print("Only found {} items, less than the maximum {}.".format(item_count, args.max_items))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--threshold", type=float, default=0.9)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--max_items", type=int, default=10000000)
    parser.add_argument("--skip_files", type=int, default=0)
    args = parser.parse_args()

    main(args)