import os
import win32com.client
import Blobconfig

# Access the shared blob service client and container client
blob_service_client = Blobconfig.blob_service_client
container_client = Blobconfig.container_client

if not blob_service_client or not container_client:
    raise Exception('BlobServiceClient or ContainerClient instance not found!')

DOWNLOADS_FOLDER_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
BLOB_CONTAINER_PATH = "AME PPI M&T Business Intelligence Folder/QAdbFiles/SQ/SQ_Portal/SQ_SAP/Boe Bi/"
FILE_IDENTIFIER = "_CONQ analysis _ details - Any fiscal year_"
NEW_FILE_NAME = "CONQ analysis _ details - Any fiscal year_2023-2024.xlsx"

def download_excel_file():
    # Launch Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6)  # 6 corresponds to the Inbox folder

    # Search for emails
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)  # Sort emails from most recent to oldest

    for message in messages:
        if "CONQ analysis & details - Any fiscal year - Automated BI extract" in message.Subject:
            attachments = message.Attachments
            for attachment in attachments:
                if FILE_IDENTIFIER in attachment.FileName:
                    attachment_path = os.path.join(DOWNLOADS_FOLDER_PATH, attachment.FileName)
                    attachment.SaveAsFile(attachment_path)

                    # Upload the file to Azure Blob Storage
                    blob_full_path = os.path.join(BLOB_CONTAINER_PATH, NEW_FILE_NAME)
                    Blobconfig.upload_to_blob_storage(attachment_path, blob_full_path)
                    
                    # Optionally, remove the local file after upload
                    os.remove(attachment_path)

                    print(f"File {attachment_path} uploaded to blob storage as {blob_full_path}")
                    return

    print("Fichier non trouvé dans la boîte de réception.")

# Execute the script
if __name__ == "__main__":
    download_excel_file()
