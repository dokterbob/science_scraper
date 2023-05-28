import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def safe_doi(doi):
    # Replace invalid characters in the DOI
    return doi.replace('/', '_')

def get_requests_session():
	# Set up a requests session with automatic retries
	session = requests.Session()
	retry = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	return session

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
