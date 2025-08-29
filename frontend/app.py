import streamlit as st
import requests
import json

st.set_page_config(page_title="Research Copilot", layout="wide")
st.title("🔬 Research Copilot with Letta")

query = st.text_input("Enter your research question:")
if st.button("Ask"):
    if query:
        # Correct URL and method
        url = "http://localhost:8000/ask"
        headers = {'Content-Type': 'application/json'}
        
        # Prepare the data payload as a dictionary
        data = {"query": query}

        try:
            # Make the POST request with the JSON data
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            # Check for a successful response
            response.raise_for_status() 
            
            # Write the full response from the backend
            st.json(response.json())
            
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            st.error("Please ensure your FastAPI backend is running with 'uvicorn main:app --reload'")
    else:
        st.warning("Please enter a research question.")