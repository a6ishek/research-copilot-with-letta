# backend/rag_manager.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from backend.letta_adapter import LettaClient
from backend.memory_manager import add_memory # Used for conversational memory

class EditableMemory:
    """A simple placeholder for MemGPT-style editable memory."""
    def __init__(self):
        self.memory_content = "This is a placeholder for editable memory."

    def get_memory(self):
        return self.memory_content

    def update(self, new_content):
        self.memory_content += "\n" + new_content

class ResearchAgent:
    def __init__(self):
        # Using a fixed-size Sentence-Transformer model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384  # Dimensionality of the embeddings for this model
        self.index = faiss.IndexFlatL2(self.dim)
        self.documents = []
        self.memory = EditableMemory()
        self.letta = LettaClient()

    def ingest(self, text: str):
        """Adds a new document to the RAG index."""
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding).astype("float32"))
        self.documents.append(text)

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """Performs a RAG search on the indexed documents."""
        if not self.documents:
            return []
        
        q_emb = self.model.encode([query]).astype("float32")
        D, I = self.index.search(q_emb, k)
        
        # Filter out invalid indices and retrieve documents
        retrieved_docs = [self.documents[i] for i in I[0] if i >= 0 and i < len(self.documents)]
        
        return retrieved_docs

    def answer(self, query: str):
        """Generates an answer using both RAG and in-memory conversation."""
        # Retrieve context from RAG
        retrieved_docs = self.retrieve(query)

        # Build combined context
        context_str = "\n".join(retrieved_docs)
        
        # Send to Letta for reasoning
        # The actual call will be handled by the memory_manager
        return self.letta.chat(query, context_str)