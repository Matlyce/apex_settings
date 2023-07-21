import getpass
import zipfile
import random
import os
import string

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def get_current_user():
    return getpass.getuser()

def zip_folder_contents(folder_path, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Using arcname, you can specify the directory structure inside the zip file
                zipf.write(file_path, arcname=os.path.relpath(file_path, folder_path))

def unzip_folder_contents(zip_path, output_folder_path):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(output_folder_path)

def get_random_value_with_interval(min_value, max_value):
    return random.randint(min_value, max_value)

def move_folder_contents(temp_path_location, source_folder_path, destination_folder_path):
    filename = "temp_" + generate_random_string(6) + ".zip"
    zip_folder_contents(source_folder_path, os.path.join(temp_path_location, filename))
    unzip_folder_contents(os.path.join(temp_path_location, filename), destination_folder_path)
    os.remove(os.path.join(temp_path_location, filename))
    