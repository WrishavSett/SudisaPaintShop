import os
import base64
import logging
import requests
from utils import get_random_color

logging.basicConfig(filename="upload-log.log", level=logging.DEBUG, 
                    filemode="w+",format="%(name)s → %(levelname)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M")

api_key = 'Token 1e0cfed5f935b1d517af3bc9048763a5d7163c2c' # Set accordingly
label_studio_url = 'http://localhost:8080/api/projects' # Set accordingly

def project_creation(project_title, project_description, label_config):
    global api_key, label_studio_url
    headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
    }
    payload = {
        "title": project_title,
        "description": project_description,
        "label_config": label_config
    }
    response = requests.post(label_studio_url, headers=headers, json=payload)
    logging.info(f"Project status code: {response.status_code}")

    if response.status_code == 201:
        print("Creating Project")
        logging.info(f"Project:{project_title} created succesfully")
    else:
        logging.error("Error in project creation")
    res = response.json()
    #print(details)
    id = res['id']
    logging.info(f"Project ID:{id} created succesfully")
    # print(id)
    return(id)

def upload_image_to_label_studio(image_path, filename, project_id, api_key, label_studio_url):
    print(image_path)
    files=[('filename',(filename,open(image_path,'rb'),'image/jpeg'))]
    payload = {}
    
    # Set up the headers
    headers = {
        "Authorization": api_key
    }

    # Make the API request
    url = f"{label_studio_url}/{project_id}/import?commit_to_project=true" #7/import?commit_to_project=true
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # Check if the request was successful
    if response.status_code == 201:
        logging.info(f"Successfully uploaded {os.path.basename(image_path)}")
    else:
        logging.error(f"Failed to upload {os.path.basename(image_path)}. Status code: {response.status_code}")
        logging.error(f"Response: {response.text}")



# Function to iterate through the output directory to upload each individual image
def upload_images_from_folder(folder_path, project_id):
    global api_key, label_studio_url
    print("Uploading Images")
    for folder in os.listdir(folder_path):    
        for filename in os.listdir(os.path.join(folder_path, folder)):
            if filename.lower().endswith(('.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, folder, filename)
                upload_image_to_label_studio(image_path, filename, project_id, api_key, label_studio_url)


def preprocess_inputs(project_title, project_description, dlabel):
    dlabstr = """"""

    view_open = """ <View>
        <Image name="image" value="$image"/>
        <RectangleLabels name="label" toName="image">"""

    view_close = """ </RectangleLabels>
        </View>"""

    for label in dlabel:
        color = get_random_color()
        dlabstr = dlabstr + f"""<Label value="{label}" background="{color}"/>""" + "\n"

    label_config = view_open + dlabstr + view_close

    return project_title, project_description, label_config

def user_input():
    project_title = input("Enter project title: ")
    project_description = input("Enter project description: ")
    
    #getting label details from the user

    dlabstr = """"""
    dlabel = []
    count = int(input("Enter the number of labels: "))
    for i in range(count):
        label,color = input("Enter the label and color separated by comma: ").split(",")
        dlabel.append((label, color))

    view_open = """ <View>
        <Image name="image" value="$image"/>
        <RectangleLabels name="label" toName="image">"""

    view_close = """ </RectangleLabels>
        </View>"""

    for label, color in dlabel:
        dlabstr = dlabstr + f"""<Label value="{label}" background="{color}"/>""" + "\n"

    label_config = view_open + dlabstr + view_close

    return project_title, project_description, label_config



if __name__ == "__main__":
    folder_path = input("Enter root directory for input: ") # Set accordingly
    project_title, project_description, label_config = user_input()
    project_id = project_creation(project_title, project_description, label_config)
    upload_images_from_folder(folder_path, project_id)