import json
import requests
import base64
import time
import asyncio
import aiohttp

async def get_json(session, access_token, entity_id, guid):
    encoded = base64.urlsafe_b64encode(entity_id.encode()).decode()
    encoded_urn = encoded.rstrip("=")
    print(f"Encoded URN: {encoded_urn}")
    
    url = f"https://developer.api.autodesk.com/modelderivative/v2/regions/eu/designdata/{encoded_urn}/metadata/{guid}/properties?forceget=true"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    retries = 0
    max_retries = 6
    wait_time = 10  # Start with a 10-second wait

    while retries < max_retries:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 202:
                    print("202 Accepted. Waiting...")
                    await asyncio.sleep(wait_time)
                    retries += 1
                    wait_time *= 2 ## total wait time = 10 + 20 + 40 + 80 + 160 + 320 = 630 seconds
                else:
                    print(f"Failed to get metadata properties: {response.status} - {response.text}")
                    return None
                
    print("Max retries reached. Failed to get metadata properties.")
    return None

   
async def main():
    from post_token import post_token
    from get_parameters import input_url, get_Folder_urn, get_project_id, get_entity_id, get_guid, get_display_name

    access_token = post_token()
    url = input_url()
    folder_urn = get_Folder_urn(url)
    project_id = get_project_id(url)
    entity_id = get_entity_id(url, project_id, access_token)
    guid = get_guid(access_token, entity_id)

    # print(f"Folder URN: {folder_urn}")  
    # print(f"Project ID: {project_id}")
    # print(f"Entity ID: {entity_id}")
    # print(f"GUID: {guid}")

    async with aiohttp.ClientSession() as session:
        json_data = await get_json(session, access_token, entity_id, guid)
        if json_data:
            formatted_json = json.dumps(json_data, indent=4)
            file_name = get_display_name()
            with open(f"{file_name}.json", "w") as file:
                file.write(formatted_json)
        else:
            print("Failed to get metadata properties.")

if __name__ == "__main__":
    asyncio.run(main())