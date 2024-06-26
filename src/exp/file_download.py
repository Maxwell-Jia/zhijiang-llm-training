import aiohttp
import asyncio
import os
from multiprocessing import Pool, cpu_count
import argparse
from urllib.parse import unquote
from tqdm import tqdm
import pandas as pd

# Function to download a single file asynchronously with retry mechanism and timeout
async def download_file(session, url, save_folder, semaphore, progress_bar, max_retries=3, timeout=3600):
    save_path = os.path.join(save_folder, os.path.basename(unquote(url)))
    async with semaphore:
        for attempt in range(max_retries):
            try:
                # Setting a timeout for the request
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    total_size = int(response.headers.get('content-length', 0))
                    with open(save_path, 'wb') as file:
                        progress_bar.reset(total=total_size)
                        async for data in response.content.iter_chunked(1024):
                            file.write(data)
                            progress_bar.update(len(data))
                # Write the successfully downloaded URL to the file
                with open("downloaded_urls.txt", "a") as log_file:
                    log_file.write(f"{url}\n")
                break  # Exit the retry loop if successful
            except (aiohttp.ClientPayloadError, aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Error downloading {url}: {e}. Retrying {attempt + 1}/{max_retries}")
                if attempt + 1 == max_retries:
                    print(f"Failed to download {url} after {max_retries} attempts.")
                    progress_bar.close()

# Coroutine to download a list of files
async def download_files(url_list, save_folder, max_concurrent_downloads, timeout):
    semaphore = asyncio.Semaphore(max_concurrent_downloads)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_list:
            progress_bar = tqdm(total=1, unit='B', unit_scale=True, desc=f"Downloading {os.path.basename(unquote(url))}")
            tasks.append(download_file(session, url, save_folder, semaphore, progress_bar, timeout=timeout))
        await asyncio.gather(*tasks)

# Function to handle multiprocessing
def download_files_process(url_list, save_folder, max_concurrent_downloads, timeout):
    asyncio.run(download_files(url_list, save_folder, max_concurrent_downloads, timeout))

# Function to split the list of URLs for multiprocessing
def split_list(input_list, n):
    k, m = divmod(len(input_list), n)
    return [
        input_list[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
    ]

def main(args):
    urls_file = args.urls_file
    save_folder = args.save_folder
    num_processes = args.num_processes
    max_concurrent_downloads = args.max_concurrent_downloads
    timeout = args.timeout

    # Load urls from file
    if urls_file.endswith(".txt"):
        with open(urls_file, 'r') as f:
            urls = f.read().splitlines()
    elif urls_file.endswith(".csv"):
        df = pd.read_csv(urls_file)
        urls = df['pdf_url'].tolist()

    # Create a folder to save downloaded files
    os.makedirs(save_folder, exist_ok=True)

    # Split URL list for multiprocessing
    url_sublists = split_list(urls, num_processes)

    # Use multiprocessing to download files with increased timeout
    with Pool(num_processes) as pool:
        results = [pool.apply_async(
            download_files_process,
            (sublist, save_folder, max_concurrent_downloads, timeout),
            error_callback=lambda e: print(f"Error: {e}")
        ) for sublist in url_sublists]

        # Wait for all processes to complete
        for result in results:
            try:
                result.get(timeout=timeout*len(urls))  # Set a timeout for each process (e.g., 1 hour)
            except TimeoutError:
                print("TimeoutError: A process took too long to complete.")

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
    parser.add_argument("--num_processes", type=int, default=1, help="Number of processes to use.")
    parser.add_argument("--max_concurrent_downloads", type=int, default=8, help="Maximum number of concurrent downloads.")
    parser.add_argument("--timeout", type=int, default=3600, help="Timeout for each download in seconds.")
    args = parser.parse_args()

    main(args)
