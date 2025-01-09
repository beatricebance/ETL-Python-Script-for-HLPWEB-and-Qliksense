from azure.storage.blob import BlobServiceClient
#from azure.identity import DefaultAzureCredential // use the credential authentification that work best for you base on the company restriction
from azure.identity import InteractiveBrowserCredential
from azure.core.exceptions import AzureError
import time


def authenticate_with_azure():
    #credential = DefaultAzureCredential()
    credential = InteractiveBrowserCredential()
    account_url = "https://sdc307184prodsto06.blob.core.windows.net"
    container_name = "usa-amemonthlygovernancefiles-ceu"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
    container_client = blob_service_client.get_container_client(container_name)
    return blob_service_client, container_client

# Authenticate and create global blob service client and container client instances
blob_service_client, container_client = authenticate_with_azure()

# Define max retries and delay for the retry mechanism
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def upload_to_blob_storage(file_path, blob_name):
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            blob_client = container_client.get_blob_client(blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"Successfully uploaded {file_path} to {blob_name}.")
            return
        except AzureError as e:
            attempts += 1
            if attempts >= MAX_RETRIES:
                error_message = f"Failed to upload {file_path} to {blob_name} after {MAX_RETRIES} attempts: {e}"
                print(error_message)
                raise Exception(error_message)
            else:
                print(f"Retry {attempts}/{MAX_RETRIES} for {file_path} to {blob_name} after error: {e}. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)

