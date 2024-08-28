import base64
import requests
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import json

# Load environment variables from .env file
load_dotenv()
# Client ID and Client Secret from .env file in the same directory
CLIENT_ID = os.getenv("FORGE_CLIENT_ID")
CLIENT_SECRET = os.getenv("FORGE_CLIENT_SECRET")
scope = "viewables:read data:read data:write data:create data:search bucket:create bucket:read bucket:update bucket:delete account:read"
grant_type = "client_credentials"
content_type = "application/x-www-form-urlencoded"

# Headers for the request
headers = {
    'Content-Type': content_type,
}
# Request token function
def post_request_token():
    url = "https://developer.api.autodesk.com/authentication/v2/token"
    data = {
        "grant_type": grant_type,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": scope,
    }
    # Send the POST request to the token endpoint
    response = requests.post(url, headers=headers, data=data)
    # Check if the request was successful
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print(f"Failed to get token: {response.status_code} - {response.text}")
        return None

# Get the access token
access_token = post_request_token()
#print(access_token)

def get_bucket_details():
    url = "https://developer.api.autodesk.com/oss/v2/buckets"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
   
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get bucket details: {response.status_code} - {response.text}")
        return None

get_bucke = get_bucket_details()
bucketKey = get_bucke['items'][0]['bucketKey']

def get_objects():
    url = f"https://developer.api.autodesk.com/oss/v2/buckets/{bucketKey}/objects"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get objects: {response.status_code} - {response.text}")
        return None
    
get_obj = get_objects()

#print (get_obj)

def chose_object():
    if not get_obj:
        print("No objects found.")
        return None
    else:
        root = tk.Tk()
        root.withdraw()
        list_of_objects = [file['objectKey'] for file in get_obj['items']]
        max_files = len(list_of_objects)
        object_number = simpledialog.askinteger("Input", f"Select the object by entering a number from 1 to {max_files}:of the list below \n" + 
                                                "\n".join(f"{i+1}. {file}" for i, file in enumerate(list_of_objects)), parent=root, minvalue=1, maxvalue=max_files)
        root.destroy()
        if object_number is not None:
            object_key = list_of_objects[object_number - 1]
            return object_key
    return None


object_key = chose_object()
#print(object_key)


def get_object_details(object_key):
    url = f"https://developer.api.autodesk.com/oss/v2/buckets/{bucketKey}/objects/{object_key}/details"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get object details: {response.status_code} - {response.text}")
        return None
    
get_obj_det = get_object_details(object_key)
get_urn = get_obj_det['objectId']
#print(get_obj_det)


def convert_urn_to_base64(urn):
    return base64.urlsafe_b64encode(urn.encode()).decode().rstrip("=")

#print(convert_urn_to_base64(get_urn))


def get_metadata():
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{convert_urn_to_base64(get_urn)}/metadata"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    # create a list meta data like name as key and guid as value
    metadata_list = []
    for i in response.json()['data']['metadata']:
        metadata_list.append({i['name']: i['guid']})
    return metadata_list

get_meta = get_metadata()



def chose_metadata():
    if not get_meta:
        print("No metadata found.")
        return None
    else:
        root = tk.Tk()
        root.withdraw()
        list_of_metadata = [list(i.keys())[0] for i in get_meta]
        max_files = len(list_of_metadata)
        metadata_number = simpledialog.askinteger("Input", f"Select the metadata by entering a number from 1 to {max_files}:of the list below \n" + 
                                                "\n".join(f"{i+1}. {file}" for i, file in enumerate(list_of_metadata)), parent=root, minvalue=1, maxvalue=max_files)
        root.destroy()
        if metadata_number is not None:
            return get_meta[metadata_number - 1]
    return None

metadata = chose_metadata()

print(metadata)


def get_metadata_properties(guid):
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{convert_urn_to_base64(get_urn)}/metadata/{guid}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get metadata properties: {response.status_code} - {response.text}")
        return None

# meta data value 

metadata_guid = list(metadata.values())[0]

def get_meta_properties(guid):
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{convert_urn_to_base64(get_urn)}/metadata/{guid}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get metadata properties: {response.status_code} - {response.text}")
        return None
    
get_meta_prop = get_meta_properties(metadata_guid)
# format the json response

def format_json(json_data):
    return json.dumps(json_data, indent=4)

print(format_json(get_meta_prop))