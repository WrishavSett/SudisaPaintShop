import os
import shutil

# Set the original folder path
folder_path = input("Enter path to your folder: ")

# Create a new folder with "_new" appended to the original folder name
new_folder_path = folder_path + "_new"
os.makedirs(new_folder_path, exist_ok=True)

# Get a sorted list of all image files in the folder
image_files = sorted(os.listdir(folder_path))

# Iterate through the images and copy every 5th image to the new folder
for i, image in enumerate(image_files):
    if (i % 5) == 0:  # Keep every 5th image (i.e., index 0, 5, 10,...)
        src_path = os.path.join(folder_path, image)
        dst_path = os.path.join(new_folder_path, image)
        shutil.copy2(src_path, dst_path)  # Copy with metadata

print("Process complete. New folder contains:", len(os.listdir(new_folder_path)), "images.")
