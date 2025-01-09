import os
import shutil
import Blobconfig

# Access the shared blob service client and container client
blob_service_client = Blobconfig.blob_service_client
container_client = Blobconfig.container_client

if not blob_service_client or not container_client:
    raise Exception('BlobServiceClient or ContainerClient instance not found!')

# Retrieve the folder path from environment variables
source_folder = os.getenv('source_folder')
destination_folder_SQ = os.getenv('destination_folder_SQ')
destination_folder_8D = os.getenv('destination_folder_8D')
destination_folder_QUALITY_PORTAL = os.getenv('destination_folder_QUALITY_PORTAL')

# Function copy to Quality Portal
def Copy_file(src, dest, filename):
    source_path = os.path.join(src, filename)
    destination_path = os.path.join(dest, filename)

    try:
        # Check if the destination file already exists
        if os.path.exists(destination_path):
            # If the file exists, remove it before copying or moving
            os.remove(destination_path)

            # Copy the CSV file from the source folder to the destination folder
            shutil.copy(source_path, destination_path)
            print(f"Copied {filename} successfully.")

    except Exception as e:
        print(f"Error occurred while processing {filename}: {e}")

# Get a list of all files in the source folder
files = os.listdir(source_folder)

# Filter out only the CSV files from the list
csv_files = [file for file in files if file.endswith('.csv')]

for file in csv_files:
    source_path = os.path.join(source_folder, file)
    
    try:
        if file in ['HLP_8D.csv', 'HLP_8D_ACTION.csv']:
            # Upload directly to the 8D folder in Blob Storage
            destination_blob_8D = os.path.join(destination_folder_8D, file)
            Blobconfig.upload_to_blob_storage(source_path, destination_blob_8D)
        else:
            # First copy to QUALITY_PORTAL
            Copy_file(source_folder, destination_folder_QUALITY_PORTAL, file)

            # Then upload to SQ
            destination_blob_SQ = os.path.join(destination_folder_SQ, file)
            Blobconfig.upload_to_blob_storage(source_path, destination_blob_SQ)

    except Exception as e:
        print(f"Error occurred while processing {file} from {source_folder}: {e}")

print("CSV files processed. All data uploaded.")
