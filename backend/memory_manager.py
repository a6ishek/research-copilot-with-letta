# backend/memory_manager.py
import os
import requests
from backend.letta_adapter import LettaClient # Import LettaClient

# Very simple in-memory storage
conversation_memory = []

def answer_with_memory(letta_client: LettaClient, agent_id: str, query: str, context: list):
    # Keep memory log
    conversation_memory.append({"role": "user", "content": query})
    
    # Build prompt
    system_prompt = f"Context: {context}\\nConversation so far: {conversation_memory}\\nAnswer the new question clearly."
    
    try:
        # Pass the agent_id to the chat method
        response_json = letta_client.chat(agent_id, query, system_prompt)
        
        # Extract the assistant's message from the JSON response
        answer = response_json.get("messages", [{}])[-1].get("content", "No response from agent.")
    except Exception as e:
        answer = f"Error calling Letta API: {e}"
    
    # Save AI response
    conversation_memory.append({"role": "assistant", "content": answer})
    return answer

def inspect_memory():
    return conversation_memory

def add_memory(content: str):
    conversation_memory.append({"role": "note", "content": content})