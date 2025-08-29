# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from backend import memory_manager
from backend.rag_manager import ResearchAgent
from backend.letta_adapter import LettaClient

app = FastAPI(title="Research Copilot API")

# Initialize Letta Client and Agent ID globally
AGENT_ID = "agent-6678aad4-8e86-4370-9255-34ad0e77d530"
letta_client = LettaClient()

# Initialize the research agent
rag_pipeline = ResearchAgent()

# Request model
class QueryRequest(BaseModel):
    query: str

# Root health check
@app.get("/")
def root():
    return {"message": "Research Copilot API running"}

# Ask endpoint
@app.post("/ask")
def ask_question(req: QueryRequest):
    # Step 1: retrieve from memory + FAISS
    context = rag_pipeline.retrieve(req.query)
    
    # Step 2: generate response with Letta (MemGPT style)
    # Pass the letta_client and agent_id to the function
    answer = memory_manager.answer_with_memory(letta_client, AGENT_ID, req.query, context)
    
    return {
        "query": req.query,
        "answer": answer,
        "context": context
    }

# Memory inspection
@app.get("/memory")
def get_memory():
    return memory_manager.inspect_memory()

# Memory update (optional)
class MemoryUpdate(BaseModel):
    content: str

@app.post("/memory")
def update_memory(update: MemoryUpdate):
    memory_manager.add_memory(update.content)
    return {"status": "memory updated", "content": update.content}