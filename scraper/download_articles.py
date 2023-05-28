import os
import requests
from tqdm import tqdm
from xml.etree import ElementTree as ET
from colorama import Fore, Style

from .common import safe_doi, get_requests_session

# Base URL for downloading Springer content
BASE_URL = 'http://link.springer.com/'

JATS_DIR = os.getenv("JATS_DIR")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")

session = get_requests_session()

def download_file(url, filename):
    """
    Download a file with progress bar
    """
    try:
        response = session.get(url, stream=True)

        file_size = int(response.headers.get('Content-Length', 0))
        progress = tqdm(response.iter_content(1024), f'Downloading {filename}', total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

        with open(filename, 'wb') as f:
            for data in progress.iterable:
                f.write(data)
                progress.update(len(data))
    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        print(f"An error occurred while downloading the file: {e}")

def parse_xml(path):
    try:
        tree = ET.parse(path, parser=ET.XMLParser(encoding='utf-8'))
        return tree.getroot()
    except ET.ParseError as e:
        print(f"ParseError: {e}")
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        error_line = lines[e.position[0]-1]  # Python uses 0-indexed, so we subtract 1
        error_column = e.position[1]
        context_range = 50  # Change this as needed
        start = max(0, error_column - context_range)
        end = min(len(error_line), error_column + context_range)
        context = error_line[start:end]

        # Highlight the error position
        context_with_error_highlighted = Fore.YELLOW + context[:context_range] + Fore.RED + context[context_range] + Fore.YELLOW + context[context_range + 1:]

        print(f"Error context: {context_with_error_highlighted}")

        raise e

def get_doi_from_jats(filename):
    """
    Parse JATS XML file and return DOI
    """

    root = parse_xml(filename)
    return root.findtext('.//article-id[@pub-id-type="doi"]')

def download_with_fallback(doi, file_type):
    url = f'{BASE_URL}{doi}.{file_type}'
    download_file_path = os.path.join(DOWNLOAD_DIR, f'{safe_doi(doi)}.{file_type}')

    if os.path.exists(download_file_path):
        print(f'{Fore.YELLOW}File {download_file_path} already exists, skipping...{Style.RESET_ALL}')
        return

    try:
        download_file(url, download_file_path)
        print(f'{Fore.GREEN}Downloaded {download_file_path}.{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Failed to download {url}. Error: {e}{Style.RESET_ALL}')
        raise

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

jats_files = [f for f in os.listdir(JATS_DIR) if f.endswith('.xml')]

for jats_file in jats_files:
    print(f'{Fore.GREEN}Processing {jats_file}...{Style.RESET_ALL}')

    doi = get_doi_from_jats(os.path.join(JATS_DIR, jats_file))

    if doi:
        try:
            download_with_fallback(doi, 'html')
        except Exception:
            print(f'{Fore.RED}HTML download failed. Trying PDF...{Style.RESET_ALL}')
            download_with_fallback(doi, 'pdf')
    else:
        print(f'{Fore.RED}No DOI found in {jats_file}.{Style.RESET_ALL}')


