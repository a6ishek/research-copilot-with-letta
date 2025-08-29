# Research-copilot-with-letta
🔬 Research Copilot: An Agentic RAG System with Letta

This project is a sophisticated Research Copilot that combines a cutting-edge Retrieval-Augmented Generation (RAG) architecture with Letta's stateful AI agents. This application showcases the principles of building an intelligent, memory-aware agent that answers questions based on a provided knowledge base and its own conversational history.

✨ Key Features
Agentic Reasoning: Powered by a Letta agent, the system exhibits more than simple text completion, using its persistent memory to provide coherent and context-aware responses.

Retrieval-Augmented Generation (RAG): The agent is "grounded" in an external knowledge base. It intelligently retrieves the most relevant information before generating a response, drastically reducing hallucinations.

Vector Database (FAISS): Utilizes the highly efficient FAISS library for ultra-fast similarity search, enabling quick retrieval of relevant documents.

Decoupled Architecture: A professionally structured project with a decoupled backend (FastAPI) and frontend (Streamlit) for clean development and independent scaling.

🧠 Architectural Overview
The project is built on a modern, decoupled architecture with a clear division of responsibilities.


Execution Flow: A User's Journey Through the System
User Query: The user enters a question in the Streamlit UI.

API Call: The frontend sends a POST request to the FastAPI backend's /ask endpoint.

Retrieval: The rag_manager converts the query to an embedding and uses FAISS to find the most relevant documents from the knowledge base.

Context Augmentation: The memory_manager combines the retrieved documents with the conversation history.

Agentic Generation: The letta_adapter sends this comprehensive prompt to the live Letta agent API. The agent processes the information, applies its reasoning, and generates a final response.

Response & Memory Update: The final response is returned from the Letta API, passed back to the main.py API, which updates the agent's short-term memory and returns the answer to the Streamlit frontend.

📸 Output Screenshots

1. Main UI
Screenshot of the Streamlit UI with the input field and "Ask" button.

2. Answer with Context
Screenshot showing a question, the final answer, and the retrieved context used to generate the answer.

3. Memory Interaction
Screenshot demonstrating how the agent remembers a past detail from the conversation.

🛠️ Getting Started
Prerequisites
Python 3.8 or higher

A Letta API Key and an existing Agent ID.

Note: The code contains a placeholder (----) for your API key. You must replace this with your actual key.

Installation
Clone the repository:

git clone https://github.com/your-username/research-copilot.git
cd research-copilot

Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Running the Application
This project requires running both the backend and frontend simultaneously in separate terminals.

Terminal 1: Start the Backend API

uvicorn main:app --reload

The API will be live at http://127.0.0.1:8000.

Terminal 2: Start the Streamlit Frontend

streamlit run app.py

The UI will open in your browser, likely at http://localhost:8501.

📄 License & Credits
This project is licensed under the MIT License.

Developed by Abishek.R
