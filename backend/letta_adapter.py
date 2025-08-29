# backend/letta_adapter.py
import requests
import json
import os

class LettaClient:
    def __init__(self, api_key=os.getenv("LETTA_API_KEY", "sk-----==")):
        self.api_key = api_key
        # The base URL is now "https://api.letta.com/v1"
        self.base_url = "https://api.letta.com/v1"

    def chat(self, agent_id: str, user_message: str, system_prompt: str):
        """
        Sends a message to a specific Letta agent.
        """
        # Correct URL using the agent_id
        url = f"{self.base_url}/agents/{agentid}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare the message payload, which expects a list of messages
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": True # Use streaming for real-time updates
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            
            # The API returns a stream of events, so you might need to handle this differently
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Letta API call failed: {e}")
            return {"response": f"Letta API call failed: {e}"}
