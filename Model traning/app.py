import os
import shutil

def move_files_between_folders(fol1, fol2):
    # Ensure both folders exist
    if not os.path.exists(fol1):
        print(f"Source folder '{fol1}' does not exist.")
        return
    if not os.path.exists(fol2):
        print(f"Destination folder '{fol2}' does not exist.")
        return

    # List all subfolders in fol1
    subfolders = [f for f in os.listdir(fol1) if os.path.isdir(os.path.join(fol1, f))]

    for subfolder in subfolders:
        source_path = os.path.join(fol1, subfolder)
        destination_path = os.path.join(fol2, subfolder)

        # Ensure the corresponding subfolder exists in fol2
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        # Move all files from the source subfolder to the destination subfolder
        for file_name in os.listdir(source_path):
            file_path = os.path.join(source_path, file_name)
            if os.path.isfile(file_path):  # Check if it's a file
                shutil.move(file_path, destination_path)
                print(f"Moved '{file_name}' from '{source_path}' to '{destination_path}'.")

if __name__ == "__main__":
    # Specify the paths to fol1 and fol2
    fol1 = "datasets"
    fol2 = "Data"

    move_files_between_folders(fol1, fol2)
