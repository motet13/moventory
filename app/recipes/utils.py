import secrets
import os
import json
from config import Config
from PIL import Image

current_dish_name = None
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
    image_path = os.path.join(f"{Config.MOVINTORY_RECIPE_IMAGE_PATH}/" + image_fn)
    
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
    # '{Config.MOVINTORY_RECIPE_PATH}/recipes_data.json'
    with open(f'{Config.MOVINTORY_RECIPE_PATH}/recipes_data.json') as file:
        data = json.load(file)

    return data

# Add or Update recipes
def dumps_recipes(data, dict=None, index: int = None, edit=False):
    if edit:
        with open(f'{Config.MOVINTORY_RECIPE_PATH}/recipes_data.json', 'w') as file:
            data['Recipes'][index].update(dict)
            file.write(json.dumps(data, indent=4))
    else:
        with open(f'{Config.MOVINTORY_RECIPE_PATH}/recipes_data.json', 'w') as file:
                data['Recipes'].append(make_recipe_input)
                file.write(json.dumps(data, indent=4))