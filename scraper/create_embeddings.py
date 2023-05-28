import os
import gzip
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

for text_file in tqdm(text_files, desc="Creating Embeddings", unit="file"):
    text_filepath = os.path.join(TEXT_DIR, text_file)
    with gzip.open(text_filepath, 'rt') as file:
        text = file.read()
        sentences = text.split('. ')

        embeddings = model.encode(sentences)
        document_embedding = embeddings.mean(axis=0)
