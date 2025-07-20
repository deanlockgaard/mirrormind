# ==============================================================================
# File: engine.py
# Description: The core logic for retrieving context and generating responses.
# ==============================================================================
import json
import os
import yaml
from datetime import datetime

# --- Constants ---
MEMORY_FILE = "memory/core_memory.json"
GOALS_FILE = "memory/goals.json"
CONSTITUTION_FILE = "user_profile/constitution.yaml"

# --- A set of common English stop words to ignore during search ---
# NOTE: This list has been expanded to improve search accuracy.
STOP_WORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can", "did", "do", "does", "doing", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if",
    "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most", "my",
    "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or",
    "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she",
    "should", "so", "some", "such", "t", "than", "that", "the", "their", "theirs",
    "them", "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
    "where", "which", "while", "who", "whom", "why", "will", "with", "you", "your",
    "yours", "yourself", "yourselves", "i'm", "thinking", "feeling", "felt", "about", "issues"
])

# --- Data Loading and Saving Functions ---
def load_json_data(filepath):
    """Safely loads data from a JSON file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def load_yaml_data(filepath):
    """Safely loads data from a YAML file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    return {}

def save_memory(user_input, assistant_reply, summary):
    """Saves a new memory entry to the JSON file."""
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

# --- Context Retrieval Functions ---
def retrieve_relevant_context(user_input, data, text_key, max_results=2):
    """
    A more robust keyword-based retrieval function.
    Finds the most recent entries that share meaningful keywords with the user_input.
    """
    # Clean the input by removing punctuation and filtering stop words
    clean_input = ''.join(c for c in user_input.lower() if c.isalnum() or c.isspace())
    keywords = set(clean_input.split()) - STOP_WORDS

    matches = []

    # Iterate backwards through the data to find the most recent matches first
    for entry in reversed(data):
        # Combine relevant text fields from the entry for matching
        entry_text_raw = ""
        if isinstance(text_key, list):
            for key in text_key:
                entry_text_raw += entry.get(key, "") + " "
        else:
            entry_text_raw += entry.get(text_key, "")

        # Clean the entry text and filter out stop words
        clean_entry_text = ''.join(c for c in entry_text_raw.lower() if c.isalnum() or c.isspace())
        entry_keywords = set(clean_entry_text.split()) - STOP_WORDS

        # Check for any overlapping meaningful keywords
        if keywords & entry_keywords:
            matches.append(entry)

        # Stop searching once we have found enough matches
        if len(matches) >= max_results:
            break

    # The matches are in reverse chronological order, so we reverse them back.
    return list(reversed(matches))

# --- Prompt Formatting Functions ---
def format_context_for_prompt(context_data, title, text_key):
    """Formats a list of context entries into a string for the prompt."""
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
    """
    The main function that orchestrates context retrieval and response generation.
    """
    # 1. Load all data sources
    memories = load_json_data(MEMORY_FILE)
    goals = load_json_data(GOALS_FILE)
    constitution = load_yaml_data(CONSTITUTION_FILE)

    # 2. Retrieve relevant context from each source
    relevant_memories = retrieve_relevant_context(user_input, memories, "summary")
    relevant_goals = retrieve_relevant_context(user_input, goals, ["name", "description"])

    # 3. Format the retrieved context into clean text blocks
    memory_context = format_context_for_prompt(relevant_memories, "Memories", "summary")
    goal_context = format_context_for_prompt(relevant_goals, "Goals", ["name", "description"])

    # 4. Construct the full prompt for the LLM
    system_prompt = f"Your persona is defined by these principles: {json.dumps(constitution, indent=2)}\n\n"
    full_prompt = system_prompt + goal_context + memory_context + f"User's current thought: {user_input}\n\nAI Companion's reflection:"

    # 5. Generate a (mock) response
    mock_reply = (
        "*(This is a mock response. The full prompt that would be sent to the LLM is shown below for testing purposes.)*\n\n"
        "--- START OF PROMPT ---\n"
        f"{full_prompt}"
        "--- END OF PROMPT ---"
    )

    # 6. Save the new interaction to memory
    save_memory(user_input=user_input, assistant_reply=mock_reply, summary=user_input)
    
    return mock_reply