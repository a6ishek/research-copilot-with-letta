# Research Copilot 🚀

This project integrates **Letta** + **MemGPT-style memory management** into a research copilot.

## Components
- **Backend**: FastAPI API (memory, RAG, Letta)
- **Frontend**: Streamlit UI
- **Memory Management**: Short-term + long-term (MemGPT inspired)

## Run

### Backend
```bash
uvicorn backend.api_main:app --reload
```

### Frontend
```bash
streamlit run frontend/app.py
```
