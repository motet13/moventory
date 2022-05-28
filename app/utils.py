import csv
import secrets
import os
import json
from config import Config
from PIL import Image


make_recipe_input = {
    "Name": None,
    "Description": None,
    "Ingredients": None,
    "Instructions": None,
    "Image": None
}

# Resize uploaded image before saving in system.
def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(f"{Config.MOVENTORY_RECIPE_IMAGE_PATH}/" + image_fn)
    
    output_size = (250, 250)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn


# Get only datas from given <dish_name>
def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


# Load recipe JSON
def load_recipes():
    with open(f'{Config.MOVENTORY_RECIPE_PATH}/recipes_data.json') as file:
        data = json.load(file)

    return data


# Add or Update recipes
def dumps_recipes(data=None, dict=None, index: int = None, edit=False, delete=False):
    if edit:
        with open(f'{Config.MOVENTORY_RECIPE_PATH}/recipes_data.json', 'w') as file:
            data['Recipes'][index].update(dict)
            file.write(json.dumps(data, indent=4))
    elif delete:
        with open(f'{Config.MOVENTORY_RECIPE_PATH}/recipes_data.json', 'w') as file:
            data['Recipes'].pop(index)
            file.write(json.dumps(data, indent=4))
    else:
        with open(f'{Config.MOVENTORY_RECIPE_PATH}/recipes_data.json', 'w') as file:
                data['Recipes'].append(dict)
                file.write(json.dumps(data, indent=4))

# Write received json object to posted_json.json file
def write_to_json_file(obj):
    with open(f'{Config.MOVENTORY_POSTED_JSON_PATH}/posted_json.json', 'w') as file:
        file.write(json.dumps(obj, indent=4))

# Load posted_json file to edit
def load_posted_json():
    with open(f'{Config.MOVENTORY_POSTED_JSON_PATH}/posted_json.json') as file:
        data = json.load(file)
    
    return data

# Get the total number of RECIPES
def total_recipes():
    data = load_recipes()
    recipe_counts = len(data['Recipes'])

    return recipe_counts

# Get the total number of schduled task
def total_task():
    schedule_file = f"{Config.MOVENTORY_SCHEDULE_PATH}/schedule.csv"
    total = 0
    if os.path.exists(schedule_file):
        with open(schedule_file, 'r') as csv_file:
            read_csv = csv.reader(csv_file)
            for count, _ in enumerate(read_csv):
                total = count

    return total
    