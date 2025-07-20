# ==============================================================================
# File: generate_embeddings.py
# Description: A script to pre-calculate and save semantic search indexes.
# ==============================================================================
import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Constants ---
MODEL_NAME = 'all-MiniLM-L6-v2'
MEMORY_FILE = "memory/core_memory.json"
GOALS_FILE = "memory/goals.json"
MEMORY_INDEX_FILE = "memory/faiss_memory_index.bin"
GOALS_INDEX_FILE = "memory/faiss_goals_index.bin"

def create_index(input_path, output_path, text_keys):
    """
    Reads a JSON file, generates embeddings for specified text keys,
    and saves a FAISS index for fast searching.
    """
    print(f"\n--- Processing {input_path} ---")
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}. Skipping.")
        return

    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {input_path}. Skipping.")
        return

    if not data:
        print(f"No data in {input_path}. Skipping.")
        return

    texts_to_embed = []
    for entry in data:
        combined_text = " ".join([entry.get(key, "") for key in text_keys])
        texts_to_embed.append(combined_text.strip())

    print(f"Generating embeddings for {len(texts_to_embed)} entries...")
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)

    embeddings = np.array(embeddings).astype('float32')
    d = embeddings.shape[1]

    index = faiss.IndexFlatL2(d)
    index = faiss.IndexIDMap(index)

    index.add_with_ids(embeddings, np.arange(len(data)))

    faiss.write_index(index, output_path)
    print(f"✅ FAISS index with {index.ntotal} vectors saved to {output_path}")

if __name__ == "__main__":
    print("Loading sentence transformer model...")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded.")

    create_index(
        input_path=MEMORY_FILE,
        output_path=MEMORY_INDEX_FILE,
        text_keys=["summary"]
    )

    create_index(
        input_path=GOALS_FILE,
        output_path=GOALS_INDEX_FILE,
        text_keys=["name", "description"]
    )