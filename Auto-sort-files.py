import os
import shutil


def organize_files(directory=None):

    if directory is None:
        directory = os.getcwd()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.exists(file_path):
            file_extension = filename.split('.')[-1].upper()
            target_folder = os.path.join(directory, file_extension)

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                
            print(f"file_extension: {file_extension}")
            print(f"target_folder: {target_folder}")
            
            target_path = os.path.join(target_folder, filename)
            
            if os.path.exists(target_path):
                os.remove(target_path)
            
            shutil.move(file_path, target_folder)

    print("Files have been organized")

# can be replaced with None and script will organize files where the script is located
directory = "D:\\Users\\Downloads" 
organize_files(directory)