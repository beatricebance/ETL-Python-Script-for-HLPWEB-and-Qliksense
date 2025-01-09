import os

folder_path = os.getenv('DATA_PATH')

def delete_all_zip_files(folder_path):
    try:
        # List all files in the specified folder
        files = os.listdir(folder_path)

        # Iterate through the files and delete all .zip files
        for file in files:
            if file.endswith(".zip"):
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)
                print(f"Deleted {file} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
