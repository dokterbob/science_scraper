import os
import gzip
import spacy
from tqdm import tqdm
from colorama import Fore, Style
from sentence_transformers import SentenceTransformer
import numpy as np

TEXT_DIR = os.getenv("TEXT_DIR")
EMBEDDINGS_DIR = os.getenv("EMBEDDINGS_DIR")

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

text_files = [f for f in os.listdir(TEXT_DIR) if f.endswith('.txt.gz')]

# Load pre-trained model for sentence embeddings
model = SentenceTransformer('all-mpnet-base-v2', device='mps')

def get_tokenizer():
    nlp = spacy.blank('en')
    nlp.add_pipe('sentencizer')
    nlp.max_length=2000000

    return nlp

tokenizer = get_tokenizer()

def get_embeddings(text):
    doc = tokenizer(text)
    sentences = [sent.text for sent in doc.sents]

    embeddings = model.encode(sentences, batch_size=8)
    return embeddings.mean(axis=0)


def embed_text(text_filepath, embedding_filepath):
    with gzip.open(text_filepath, 'rt') as file:
        text = file.read()

        document_embedding = get_embeddings(text)

        # Save the embeddings to a .npy file
        np.save(embedding_filepath, document_embedding)


for text_file in tqdm(text_files, desc="Creating Embeddings", unit="file"):
    text_filepath = os.path.join(TEXT_DIR, text_file)
    embedding_filepath = os.path.join(EMBEDDINGS_DIR, text_file.replace('.txt.gz', '.npy'))

    if os.path.exists(embedding_filepath):
        print(f'{Fore.YELLOW}File {Fore.BLUE}{embedding_filepath}{Fore.YELLOW} already exists, skipping...{Style.RESET_ALL}')
        continue

    try:
        embed_text(text_filepath, embedding_filepath)
    except Exception as e:
        print(f'{Fore.RED}Error embedding {Fore.BLUE}{text_filepath}{Fore.RED}: {e}{Style.RESET_ALL}')
        raise e
