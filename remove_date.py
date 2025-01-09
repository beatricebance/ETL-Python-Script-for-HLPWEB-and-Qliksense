import os
import re
import shutil
import zipfile

def extract_and_rename_csv(zip_file, csv_folder):
    """
    Extract all .csv files from a .zip archive, rename and save them to the csv_folder
    :param zip_file: The path to the .zip archive
    :param csv_folder: The path to the directory where extracted and renamed .csv will be saved
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for filename in zip_ref.namelist():
            if filename.endswith(".csv") and re.match(r".*\d{8}\.csv", filename):
                csv_file = zip_ref.extract(filename, csv_folder)
                
                new_filename = filename[:-13] + ".csv"
                new_file_path = os.path.join(csv_folder, new_filename)
                if not os.path.exists(new_file_path):
                    os.rename(csv_file, new_file_path)
                    print(f"{filename} => {new_filename}")

def main():
    zip_folder = "zip"
    csv_folder = "csv"
    if os.path.exists(csv_folder):
        shutil.rmtree(csv_folder)
    os.makedirs(csv_folder)
    for filename in os.listdir(zip_folder):
        if filename.endswith(".zip"):
            zip_file = os.path.join(zip_folder, filename)
            extract_and_rename_csv(zip_file, csv_folder)
            print("Main de remove_data")
if __name__ == "__main__":
    main()
