import os
import gzip

from tqdm import tqdm
from colorama import Fore, Style
from trafilatura import extract

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
TEXT_DIR = os.getenv("TEXT_DIR")

os.makedirs(TEXT_DIR, exist_ok=True)

filenames = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.html')]
for filename in tqdm(filenames, desc="Converting", unit="file", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    textpath = os.path.join(TEXT_DIR, os.path.splitext(filename)[0] + '.txt.gz')

    if os.path.exists(textpath):
        print(f'{Fore.YELLOW}File {textpath} already exists, skipping...{Style.RESET_ALL}')
        continue

    with open(filepath, "r") as file:
        html = file.read()
        text = extract(html)

        with gzip.open(textpath, "wt") as outfile:
            outfile.write(text)
