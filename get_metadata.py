from post_token import post_token
from get_parameters import input_url, get_Folder_urn, get_project_id, get_entity_id, get_guid, get_display_name
import json
import requests
import base64
import time

def get_json(access_token, urn, guid):
    encoded = base64.urlsafe_b64encode(urn.encode()).decode()
    encoded_urn = encoded.rstrip("=")
    print(f"Encoded URN: {encoded_urn}")
    url = f"https://developer.api.autodesk.com/modelderivative/v2/regions/eu/designdata/{encoded_urn}/metadata/{guid}/properties" 
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 202:
            print(f"Metadata processing (attempt {retry_count + 1}/{max_retries}), waiting for it to be ready...")
            time.sleep(10)
            retry_count += 1
        else:
            print(f"Failed to get metadata properties: {response.status_code} - {response.text}")
            return None
    
    print("Max retries reached. Metadata is still not ready.")
    return None
    
def main():

    access_token = post_token()
    url = input_url()
    #name_of_file = get_name_of_file(url)
    folder_urn = get_Folder_urn(url)
    project_id = get_project_id(url)
    entity_id = get_entity_id(url, project_id, access_token)
    guid = get_guid(access_token, entity_id)

    print(f"Folder URN: {folder_urn}")  
    print(f"Project ID: {project_id}")
    print(f"Entity ID: {entity_id}")
    print(f"GUID: {guid}")
    #print(f"Name of file: {name_of_file}")

    json_data = get_json(access_token, entity_id, guid)
    if json_data:
        formatted_json = json.dumps(json_data, indent=4)
       
        # create a json file as output in the same directory with the name of the 
        # set the name of the file as the name of the file in the metadata
        file_name = get_display_name()
        with open(f"{file_name}.json", "w") as file:
            file.write(formatted_json)
        
    else:
        print("Failed to get metadata properties.")

  
if __name__ == "__main__":

    main()
    
