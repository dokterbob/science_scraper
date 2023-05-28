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
