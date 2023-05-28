import os
import gzip
import spacy
from tqdm import tqdm
from colorama import Fore, Style
from sentence_transformers import SentenceTransformer

TEXT_DIR = os.getenv("TEXT_DIR")
EMBEDDINGS_DIR = os.getenv("EMBEDDINGS_DIR")

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

text_files = [f for f in os.listdir(TEXT_DIR) if f.endswith('.txt.gz')]
skipped_files = []

# Load pre-trained model for sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2', device='mps:0')

def get_tokenizer():
    from spacy.cli import download

    try:
        # Try to load the model
        return spacy.load('en_core_web_sm')
    except OSError:
        # If model is not found, download it
        print("Model not found. Downloading...")
        download('en_core_web_sm')
        # Load the model after downloading
        return spacy.load('en_core_web_sm')

tokenizer = get_tokenizer()

for text_file in tqdm(text_files, desc="Creating Embeddings", unit="file"):
    text_filepath = os.path.join(TEXT_DIR, text_file)
    with gzip.open(text_filepath, 'rt') as file:
        text = file.read()
        doc = tokenizer(text)
        sentences = [sent.text for sent in doc.sents]

        embeddings = model.encode(sentences)
        document_embedding = embeddings.mean(axis=0)
