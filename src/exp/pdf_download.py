import aiohttp
import asyncio
import os
from multiprocessing import Pool, cpu_count
import argparse
from urllib.parse import unquote


# Function to download a single file asynchronously
async def download_file(session, url, save_folder):
    async with session.get(url) as response:
        filename = unquote(url.split('/')[-1])
        save_path = os.path.join(save_folder, filename)

        if os.path.exists(save_path):
            print(f"File {filename} already exists. Skipping download.")
            return
        
        with open(filename, "wb") as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Downloaded: {url}")


# Coroutine to download a list of files
async def download_files(url_list, save_folder):
    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url, save_folder) for url in url_list]
        await asyncio.gather(*tasks)


# Function to handle multiprocessing
def download_files_process(url_list, save_folder):
    asyncio.run(download_files(url_list, save_folder))


# Function to split the list of URLs for multiprocessing
def split_list(input_list, n):
    k, m = divmod(len(input_list), n)
    return [
        input_list[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
    ]


def main(args):
    urls_file: str = args.urls_file
    save_folder: str = args.save_folder
    num_processes: int = args.num_processes

    # Load urls from file
    if urls_file.endswith(".txt"):
        with open(urls_file, 'r') as f:
            urls = f.read().splitlines()
    elif urls_file.endswith(".csv"):
        import pandas as pd
        df = pd.read_csv(urls_file)
        urls = df['pdf_url'].tolist()

    # Create a folder to save downloaded files
    os.makedirs(save_folder, exist_ok=True)

    # Split URL list for multiprocessing
    url_sublists = split_list(urls, num_processes)

    # Use multiprocessing to download files
    with Pool(num_processes) as pool:
        pool.starmap(
            download_files_process,
            [(sublist, save_folder) for sublist in url_sublists],
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download files asynchronously using multiprocessing."
    )
    parser.add_argument(
        "--urls_file",
        type=str,
        required=True,
        help=("The file that records the URL list. ",
              "If it is a .txt file, each line must contain a separate URL. ",
              "If it is a csv file, it must contain a column named `pdf_url`."),
    )
    parser.add_argument("--save_folder", type=str, required=True, help="Folder to save downloaded files.")
    parser.add_argument("--num_processes", type=int, default=4, help="Number of processes to use.")
    args = parser.parse_args()

    main(args)
