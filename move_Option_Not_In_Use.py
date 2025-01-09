import os
import shutil
import Blobconfig

# Access the shared blob service client and container client
blob_service_client = Blobconfig.blob_service_client
container_client = Blobconfig.container_client

if not blob_service_client or not container_client:
    raise Exception('BlobServiceClient or ContainerClient instance not found!')

def move_files(files_to_move, source_folder, destination_folder, use_azure=False):
    # If files_to_move is a string, convert it to a list containing that string
    if isinstance(files_to_move, str):
        files_to_move = [files_to_move]

    for file_name in files_to_move:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        # Check if the source file exists
        if os.path.exists(source_path):
            try:
                if use_azure:
                    # Uploading to Azure Blob Storage
                    Blobconfig.upload_to_blob_storage(source_path, destination_path)
                else:
                    # Check if the destination file already exists
                    if os.path.exists(destination_path):
                        # If the file exists, delete it before copying the new file
                        os.remove(destination_path)
                        print(f"Deleted existing file at {destination_path}.")
                    
                    # Copy the file from the source folder to the destination folder
                    shutil.copy(source_path, destination_path)
                    print(f"Copied {file_name} successfully to {destination_folder}.")
            except Exception as e:
                print(f"Error occurred while processing {file_name}: {e}")
        else:
            print(f"{file_name} does not exist in the source directory.")