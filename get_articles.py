import time
import os
import xml.etree.ElementTree as ET

from tqdm import tqdm
from colorama import Fore, init

from .secrets import api_key
from .common import safe_doi, get_requests_session

init(autoreset=True) # to reset colorama color settings after each print

# query = "issn:1572-9680" # Agroforestry Systems
# query = "keyword:agroforestry"
# query = "keyword:forestry"
# query = "keyword:soil"
# query = "keyword:fungi"
# query = "keyword:ecology"
# query = "keyword:forest"
# query = "keyword:regeneration"
# query = "keyword:biodiversity"
# query = "keyword:climate"
# query = "keyword:plants"
# query = "keyword:permaculture"
# query = "keyword:agroecology"
query = "keyword:taxonomy"

base_url = "http://api.springernature.com/openaccess/jats"

wait_time = 2 # Seconds between requests

# Create a directory to store the XML files
os.makedirs('jats_files', exist_ok=True)

session = get_requests_session()

def get_articles(query, api_key, start_record=1, records_per_request=25):
    params = {
        "q": query,
        "p": records_per_request,
        "s": start_record,
        "api_key": api_key
    }

    while True:
        response = session.get(base_url, params=params)
        print(Fore.BLUE + f'Received {response.status_code} response from API')

        if response.status_code != 200:
            raise Exception("Unexpected response code")

        # Parse the XML response
        root = ET.fromstring(response.text)

        # Extract individual documents from the response
        articles = root.findall('.//article')
        if not articles:
            print(Fore.RED + f'No articles returned, breaking off.')
            break

        for article in articles:
            yield ET.tostring(article, encoding='utf8').decode('utf8')

        # Wait between requests to respect rate limits
        time.sleep(wait_time)

        # Update the start record for the next batch of articles
        params["s"] += records_per_request



for i, article_xml in enumerate(tqdm(get_articles(query, api_key), desc="Downloading articles"), start=1):
    # Extract the DOI from the article XML
    article_root = ET.fromstring(article_xml)
    doi = article_root.findtext('.//article-id[@pub-id-type="doi"]')

    # Create a unique filename for each article using the safe DOI
    filename = os.path.join('jats_files', f'{safe_doi(doi)}.xml')

    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(article_xml)
        print(Fore.CYAN + f"Wrote article with DOI {doi} to {filename}")
    else:
        print(Fore.YELLOW + f"File for article with DOI {doi} already exists. Skipping.")
