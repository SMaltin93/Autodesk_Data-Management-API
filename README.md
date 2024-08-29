
# Autodesk Forge Metadata Fetcher

This Python script fetches metadata properties from the Autodesk Forge API using a model's URN and GUID. The retrieved metadata is saved as a JSON file, with the filename based on the model's display name.

## Prerequisites

Before using this script, ensure you have the following:

1. **Autodesk Forge API credentials**:
   - [Forge Client ID](https://forge.autodesk.com/myapps/)
   - [Forge Client Secret](https://forge.autodesk.com/myapps/)

2. **Python 3.x** installed on your machine.

3. Required Python packages:
   - `requests`
   - `python-dotenv`

## Setup

1. **Clone or Download the repository**:

   - **Download as a ZIP file**:

     If you prefer, you can download the repository as a ZIP file:
     
     1. Go to the [repository page](https://github.com/SMaltin93/forge-metadata-fetcher-API).
     2. Click the "Code" button.
     3. Select "Download ZIP".
     4. Extract the ZIP file to your desired location.
     5. Navigate to the extracted folder in your terminal:

2. **Create and configure the `.env` file**:

   In the root directory of the project, create a `.env` file and add your Autodesk Forge credentials:

   ```bash
   touch .env
   ```
   OBS, you can skip this step if you have .env-file. 


   Edit the `.env` file and add the following lines:

   ```plaintext
   FORGE_CLIENT_ID=your_client_id
   FORGE_CLIENT_SECRET=your_client_secret
   ```

   Replace `your_client_id` and `your_client_secret` with your actual Autodesk Forge Client ID and Client Secret.

3. **Install dependencies**:

   Use `pip` to install the necessary Python packages:

```bash
   python.exe -m pip install --upgrade pip
   ```
   
   ```bash
   pip install python-dotenv
   ```

    ```bash
   pip install requests
   ```

    ```bash
   pip install aiohttp
   ```

## Usage

1. **Run the script**:

   To execute the script, run the following command in your terminal:

   ```bash
   python get_metadata.py
   ```

   Replace `get_metadata.py` with the actual name of your script file.

2. **Input the URL**:

   The script will prompt you to input a URL related to your Autodesk project. The URL is used to extract various identifiers required for fetching metadata.

3. **Output**:

   The script will fetch the metadata and save it as a JSON file in the json_files directory. The JSON file will be named according to the display name of the model retrieved from the Autodesk Forge API.

   For example, if the model's display name is `ExampleModel`, the output file will be `ExampleModel.json`.

## Script Overview

### Main Components

- **`post_token.py`**: Handles authentication and returns an access token for the Autodesk Forge API.
- **`get_parameters.py`**: Contains functions to extract URN, Project ID, Entity ID, and GUID from the input URL.
- **`get_json` function**: Encodes the URN, constructs the API request, and fetches metadata properties.

### Retry Mechanism

The script includes a retry mechanism that will attempt to fetch metadata properties up to 10 times if the metadata is still processing.

## Example Output

After running the script, you will find a JSON file in your directory named after the model's display name, which will contain the fetched metadata properties in a structured JSON format.

## Troubleshooting

- **Authentication Errors**: Ensure that your Forge Client ID and Client Secret are correctly set in the `.env` file.
- **Metadata Processing Delays**: The script retries up to 10 times, with a 10-second delay between each attempt, to account for any delays in metadata processing.
