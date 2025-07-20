# ==============================================================================
# File: engine.py
# Description: The core logic, now upgraded to use semantic search.
# ==============================================================================
import json
import os
import yaml
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Load environment variables ---
load_dotenv()

# --- Constants ---
MEMORY_FILE = "memory/core_memory.json"
GOALS_FILE = "memory/goals.json"
CONSTITUTION_FILE = "user_profile/constitution.yaml"
MEMORY_INDEX_FILE = "memory/faiss_memory_index.bin"
GOALS_INDEX_FILE = "memory/faiss_goals_index.bin"
MODEL_NAME = 'all-MiniLM-L6-v2' # The local model for embeddings

# --- Initialize Models ---
print("Engine: Loading local sentence transformer model for embeddings...")
embedding_model = SentenceTransformer(MODEL_NAME)
print("Engine: Embedding model loaded.")

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    llm_model = genai.GenerativeModel('gemini-1.5-flash')
    print("Engine: Gemini API configured successfully.")
except Exception as e:
    print(f"Engine: Error configuring Gemini API: {e}")
    llm_model = None

# --- Data Loading and Saving Functions ---
def load_json_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def load_yaml_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    return {}

def save_memory(user_input, assistant_reply, summary):
    memories = load_json_data(MEMORY_FILE)
    new_memory = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_input": user_input,
        "assistant_reply": assistant_reply,
        "summary": summary,
        "themes": []
    }
    memories.append(new_memory)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memories, f, indent=2)

# --- Semantic Context Retrieval ---
def search_index(query_embedding, index, data, max_results, threshold=0.5):
    """Core search logic that filters results by a similarity threshold."""
    distances, indices = index.search(query_embedding, max_results)

    matches = []
    if indices.size > 0:
        for i, dist in zip(indices[0], distances[0]):
            if i != -1:
                similarity = 1 / (1 + dist)
                if similarity >= threshold:
                    matches.append(data[i])
    return matches

def retrieve_relevant_context(user_input, data, index_path_or_obj, max_results=2, threshold=0.5):
    """Retrieves context using a FAISS index, accepting a path or a pre-loaded object."""
    if not data:
        return []

    index = None
    if isinstance(index_path_or_obj, str):
        if not os.path.exists(index_path_or_obj):
            return []
        index = faiss.read_index(index_path_or_obj)
    else:
        index = index_path_or_obj

    query_embedding = embedding_model.encode([user_input])
    return search_index(query_embedding, index, data, max_results, threshold=threshold)

# --- Prompt Formatting ---
def format_context_for_prompt(context_data, title, text_key):
    if not context_data:
        return ""

    formatted_texts = []
    for item in context_data:
        if isinstance(text_key, list):
             formatted_texts.append(f"- {item.get(text_key[0], '')}: {item.get(text_key[1], '')}")
        else:
            formatted_texts.append(f"- {item.get(text_key, '')}")

    context_block = "\n".join(formatted_texts)
    return f"--- Relevant {title} ---\n{context_block}\n-------------------------\n\n"

# --- Main Engine Function ---
def get_response(user_input):
    if not llm_model:
        return "Error: Gemini API is not configured. Please check your API key."

    memories = load_json_data(MEMORY_FILE)
    goals = load_json_data(GOALS_FILE)
    constitution = load_yaml_data(CONSTITUTION_FILE)

    relevant_memories = retrieve_relevant_context(user_input, memories, MEMORY_INDEX_FILE)
    relevant_goals = retrieve_relevant_context(user_input, goals, GOALS_INDEX_FILE)

    memory_context = format_context_for_prompt(relevant_memories, "Memories", "summary")
    goal_context = format_context_for_prompt(relevant_goals, "Goals", ["name", "description"])

    system_instruction = f"Your persona is AI Companion. Adhere strictly to these principles: {json.dumps(constitution, indent=2)}"
    user_prompt = goal_context + memory_context + f"User's current thought: {user_input}\n\nAI Companion's reflection:"

    try:
        full_prompt = [{'role':'user', 'parts': [system_instruction, user_prompt]}]
        print("="*50 + "\nPROMPT SENT TO GEMINI API:\n" + "="*50 + f"\n{user_prompt}\n" + "="*50)

        response = llm_model.generate_content(full_prompt)
        final_reply = response.text
    except Exception as e:
        print(f"An error occurred during API call: {e}")
        final_reply = "I'm sorry, I encountered an error while trying to think. Please check the console for details."

    save_memory(user_input=user_input, assistant_reply=final_reply, summary=user_input)

    return final_reply