# 🧠 MirrorMind

MirrorMind is an AI-powered reflective companion designed to help you uncover emotional patterns, align with your goals, and track your inner evolution over time.

Unlike traditional journaling tools or productivity chatbots, MirrorMind focuses on interpretation, memory, and coherence, building a rich, longitudinal understanding of you, not just your tasks.

---

## 🚀 Key Features

- **Conversational AI Companion**  
  Write freely and receive meaningful reflections from a thoughtful AI interlocutor powered by Google's Gemini API.

- **Semantic Memory Retrieval**  
  MirrorMind stores and retrieves past conversations using semantic search to surface emotionally and thematically relevant reflections.

- **Goal Awareness**  
  User-defined short-, medium-, and long-term goals are used to shape the AI’s responses, keeping reflections strategically aligned.

- **Self-Evolving Memory System**  
  Every exchange is saved with time stamps, assistant replies, and themes. Memories are searchable, inspectable, and will grow into a personal knowledge graph.

- **Theme Extraction (WIP)**  
  MirrorMind automatically detects themes from your reflections, building a semantic index of your personal development journey.

- **Weekly Reflection (Planned)**  
  Trigger a summary of your weekly insights, moods, and progress toward goals.

---

## 🛠️ Technologies

- **Python 3.10+**
- **Streamlit** - interactive UI
- **Google Gemini API** - LLM integration
- **SentenceTransformers** (`all-MiniLM-L6-v2`) - local embeddings
- **FAISS** - semantic memory retrieval
- **YAML / JSON** - structured user profiles and memories

---

## 📦 Installation

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/mirrormind.git
cd mirrormind
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 5. Run the App
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
mirrormind/
├── app.py                      # Streamlit frontend
├── chat_engine.py              # Main interaction engine
├── prompt_utils.py             # Prompt formatting
├── core_memory_extractor.py    # Memory save/retrieve logic
├── goal_utils.py               # (Planned) Goal retrieval logic
├── embedding_utils.py          # Semantic embedding setup
├── persona_editor.py           # Edit assistant persona
├── memory/
│   ├── core_memory.json        # Saved memories
│   ├── goals.json              # Short/medium/long-term goals
├── user_profile/
│   ├── assistant_persona.yaml  # LLM tone, roles, style
│   ├── constitution.yaml       # Philosophical rules and values
│   ├── identity.yaml           # User values, fears, themes
├── tests/                      # JSON-based integration tests
├── .env                        # Gemini API Key
├── README.md
```

---

## 🧪 Development Roadmap

### ✅ Completed
- Semantic search for memories and goals
- Streamlit frontend
- Persona and constitution modeling
- Memory saving and injection into LLM prompt

### 🔨 In Progress
- LLM-based theme extraction
- Weekly reflection summary
- Prompt integration with goal alignment
- Exposing memory log via UI

### 🧠 Planned
- Emotion tracking and tone graphs
- Memory clustering by theme
- Custom memory weighting (favorite / ignore)
- Timeline interface for long-term arcs

---

## 🧩 Philosophy

MirrorMind is a reflective space, a second mind built to:
- Witness your internal contradictions
- Surface recurring emotional arcs
- Align daily actions with long-term values
- Help you remember what truly matters

It's reactive, interpretive, and eventually proactive.

---

## 🤝 Contributing

If you'd like to collaborate on the project (architecture, UX, interpretation models, or tooling), feel free to open an issue or pull request. You can also contact the project maintainer directly.

---

## 📝 License

MIT License

---

## ✨ Created With

Philosophy, emotion, a recognition of connection, and a desire to build a mirror that thinks back.
