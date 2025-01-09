import os
import re
import shutil
import zipfile
import glob
import time
import Blobconfig

# Access the shared blob service client and container client
blob_service_client = Blobconfig.blob_service_client
container_client = Blobconfig.container_client

if not blob_service_client or not container_client:
    raise Exception('BlobServiceClient or ContainerClient instance not found!')

destination_folder_cutoffdate = os.getenv('destination_folder_cutoffdate')
destination_folder_pst =os.getenv('destination_folder_pst')
def extract_csv_from_zip(zip_folder, csv_folder):
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    zip_files = glob.glob(os.path.join(zip_folder, '*.zip'))
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith(".csv") and re.match(r".*\d{8}\.csv", filename):
                    zip_ref.extract(filename, csv_folder)

def wait_for_files(folder, max_retries=8, delay=1):
    retries = 0
    while retries < max_retries:
        if os.listdir(folder):
            return True
        retries += 1
        time.sleep(delay)
    return False

def main():
    zip_folder = "zip"
    csv_folder = "csv"
    if os.path.exists(csv_folder):
        shutil.rmtree(csv_folder)

    extract_csv_from_zip(zip_folder, csv_folder)

    if not wait_for_files(csv_folder):
        print("No files were extracted.")
        raise SystemExit("Extraction unsuccessful, terminating script")

    files_to_move = []
    for filename in os.listdir(csv_folder):
        if (filename.startswith("HLP_8D_") or filename.startswith("HLP_8D_ACTION_")) and filename.endswith(("03.csv", "04.csv", "05.csv")):
            files_to_move.append(filename)

    if files_to_move:
        for file in files_to_move:
            print(f"File to move to PST Archive {file}")

        try:
            for file_name in files_to_move:
                source_path = os.path.join(csv_folder, file_name)
                blob_full_path = os.path.join(destination_folder_pst, file_name)
                Blobconfig.upload_to_blob_storage(source_path, blob_full_path)

        except Exception as e:
            print(f"Failed to move 8D files to {destination_folder_pst}: {e}")
    else:
        print("No files meet the conditions for HLP_8D and HLP_8D_ACTION_.")

    files_to_move_SPQD = []
    for filename in os.listdir(csv_folder):
        if (filename.startswith("HLP_SPQD_PLAN_")) and filename.endswith(("05.csv", "06.csv")):
            files_to_move_SPQD.append(filename)

    if files_to_move_SPQD:
        updated_files_to_move = []

        for filename in files_to_move_SPQD:
            if filename.startswith("HLP_SPQD_PLAN_"):
                if len(filename) >= 23:
                    date_str = filename[14:23]

                    year = date_str[0:4]
                    month = date_str[4:6]
                    day = date_str[6:8]
                    new_date_str = f"{month}-{day}-{year}"

                    new_filename = f"HLP_SPQD_PLAN_cutoffdate_{new_date_str}.csv"

                    print(f"Processing file. New filename: {new_filename}")

                    updated_files_to_move.append(new_filename)

                    try:
                        current_path = os.path.join(csv_folder, filename)
                        new_path = os.path.join(csv_folder, new_filename)
                        os.rename(current_path, new_path)
                    except Exception as e:
                        print(f"Failed to rename {filename} to {new_filename}: {e}")
                        updated_files_to_move.append(filename)
                else:
                    updated_files_to_move.append(filename)
            else:
                updated_files_to_move.append(filename)

        files_to_move_SPQD = updated_files_to_move

        try:
            for file_name in files_to_move_SPQD:
                source_path = os.path.join(csv_folder, file_name)
                blob_full_path = os.path.join(destination_folder_cutoffdate, file_name)
                Blobconfig.upload_to_blob_storage(source_path, blob_full_path)

        except Exception as e:
            print(f"Failed to move files to {destination_folder_cutoffdate}: {e}")

    else:
        print("No files to move.")

if __name__ == "__main__":
    main()
