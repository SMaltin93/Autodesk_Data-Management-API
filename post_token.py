import requests
from dotenv import load_dotenv
import os

load_dotenv()

def post_token(): 
    url = "https://developer.api.autodesk.com/authentication/v2/token"
    
    # Headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Data (payload)
    data = {
        "client_id": os.getenv("FORGE_CLIENT_ID"),
        "client_secret": os.getenv("FORGE_CLIENT_SECRET"),
        "grant_type": "client_credentials",
        "scope": "viewables:read data:read data:search bucket:read account:read",
        "redirect_uri": "http://localhost:8080/oauth/callback"
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print(f"Failed to get token: {response.status_code} - {response.text}")
        return None
    

