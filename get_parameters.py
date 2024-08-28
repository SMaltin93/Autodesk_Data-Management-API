import base64
import requests
from dotenv import load_dotenv
import tkinter as tk
from tkinter import simpledialog, messagebox
from urllib.parse import urlparse, parse_qs, unquote, quote


display_name = None 

def input_url():
    root = tk.Tk()
    root.withdraw()
    url = simpledialog.askstring(title="URL", prompt="Enter the URL of the project:")
    return url

def get_display_name():
    return display_name


def get_Folder_urn(url):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    if 'folderUrn' in query_params:
        return query_params['folderUrn'][0]
    else:
        # show error message
        messagebox.showerror("No folder URN", "No folder URN found in the URL.")
        return None

def get_project_id(url):
    parsed = urlparse(url)
    path_segments = parsed.path.split('/')
    
    # The project ID should be right after '/projects/'
    try:
        project_index = path_segments.index('projects') + 1
        return path_segments[project_index]
    except ValueError:
        # Show error message if 'projects' is not in the path
        messagebox.showerror("Invalid URL", "Could not extract project ID from the URL.")
        return None
    
    
def get_entity_id(url, project_id, access_token):
    global display_name
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    print("query_params: ", query_params)
    if 'entityId' in query_params:
        entityId_urn = query_params['entityId'][0]

        print("entityId_urn: ", entityId_urn)
        # check if the entityId include 'versions' 
        if 'version' in entityId_urn:
            return entityId_urn
        api_url = f"https://developer.api.autodesk.com/data/v1/projects/b.{project_id}/items/{entityId_urn}/versions"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(api_url, headers=headers)
        # gain the id of the entity from derivatives id 
        if response.status_code == 200:
            # set 'displayName'
            display_name = response.json()['data'][0]['attributes']['displayName']
            print("display_name: ", display_name)
            get_display_name() 
            entity_id = response.json()['data'][0]['id']
            return entity_id
        else:
            # Show error message
            messagebox.showerror("Failed to get entity ID", f"Failed to get entity ID: {response.status_code} - {response.text}")
            return None
        

def get_guid(access_token, urn):
    # encode the urn
    encoded = base64.urlsafe_b64encode(urn.encode()).decode()
    encoded_urn = encoded.rstrip("=")
    
    url = f"https://developer.api.autodesk.com/modelderivative/v2/regions/eu/designdata/{encoded_urn}/metadata"
    print(url)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        metadata_list = []
        for i in response.json()['data']['metadata']:
            metadata_list.append({i['name']: i['guid']})
        # ruturn the guid of the first metadata
        return list(metadata_list[0].values())[0]
    else:
        print(f"Failed to get metadata: {response.status_code} - {response.text}")
        return None
    