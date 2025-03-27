import os

def delete_alternate_images(folder_path):
    # List all files in the folder
    files = sorted(os.listdir(folder_path))
    
    # Filter out non-image files (you can add more extensions if needed)
    image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Delete every alternate image
    for i in range(1, len(image_files), 2):
        os.remove(os.path.join(folder_path, image_files[i]))
        print(f"Deleted {image_files[i]}")

# Example usage
folder_path = f'./products/New Folder'
delete_alternate_images(folder_path)