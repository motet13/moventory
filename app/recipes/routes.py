from crypt import methods
import json
import re
from os import path, remove
from textwrap import indent
from flask import render_template, flash, abort, request, url_for
from flask.helpers import make_response
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from app.recipes.forms import RecipeForm
from app.utils import save_image, build_dict, load_recipes, make_recipe_input, \
    dumps_recipes, write_to_json_file, load_posted_json
from flask_login import current_user, login_required
from flask import Blueprint
from config import Config


recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes-page', methods=['GET'])
def recipes_page():
    return render_template('recipes.html', data=load_recipes())


@recipes.route('/recipes-page/edit/image', methods=['POST'])
@login_required
def edit_recipe_image():
    old_name = make_recipe_input['Image']
    if len(request.files) > 0:
        data=load_recipes()
        d_name = build_dict(data['Recipes'], key="Name")
        idx = int(d_name.get(make_recipe_input['Name'])['index'])
        image_file = save_image(request.files['imageFile'])
        make_recipe_input['Image'] = image_file
    else:
        image_file = 'default.jpg'
        make_recipe_input['Image'] = image_file

    image_path = path.join(f"{Config.MOVINTORY_RECIPE_IMAGE_PATH}/" + old_name)
    
    if old_name != 'default.jpg':
        remove(image_path)

    dumps_recipes(data=data, dict=make_recipe_input, index=idx, edit=True)
    return {"response": "Got File"}


@recipes.route('/recipes-page/edit/<dish_name>', methods=['GET', 'POST'])
@login_required
def edit_recipe_dish(dish_name):
    data=load_recipes()
    d_name = build_dict(data['Recipes'], key="Name")
    form = RecipeForm()
    idx = int(d_name.get(dish_name)['index'])
    response_data = d_name[dish_name]
    dish_img = f'images/{response_data["Image"]}'

    if request.method == 'POST': 
        if request.is_json:
            received_json = request.get_json()
            try:
                dish_name = received_json['New_Name']
            except KeyError:
                dish_name = received_json['Name']

            make_recipe_input['Name'] = dish_name
            make_recipe_input['Description'] = received_json['Description']
            make_recipe_input['Ingredients'] = received_json['Ingredients']
            make_recipe_input['Instructions'] = received_json['Instructions']
            make_recipe_input['Image'] = received_json['Image']

            dumps_recipes(data=data, dict=make_recipe_input, index=idx, edit=True)
            return make_response(f'{{"response": "{dish_name} has been updated."}}')

    return render_template('edit_recipe.html', form=form, name=dish_name,
        edit=True, response_data=response_data, dish_img=dish_img)


@recipes.route('/recipes-page/recipe-maker', methods=['GET', 'POST'])
def recipe_maker():
    form = RecipeForm()
    loaded_recipes = load_recipes()

    if request.method == 'POST':
        if request.is_json:
            received_json = request.get_json()
            write_to_json_file(obj=received_json)

            return {"response": received_json}
        else:
            data = load_posted_json()
            if len(request.files) > 0:
                image_file = save_image(request.files['imageFile'])
                data['Image'] = image_file
            else:
                write_to_json_file(obj=data)

            dumps_recipes(data=loaded_recipes, dict=data)

            return make_response(f'{{"response": "{data["Name"]} has been added."}}')

    return render_template('recipe_maker.html', form=form)


@recipes.route('/recipes-page/<dish_name>', methods=['GET'])
def recipe_dish(dish_name):
    data=load_recipes()

    # Get all dish names and check if given name is true
    dish_names = [item.get('Name') for item in data['Recipes']]

    # abort 404 if dish_name does not exist.
    if dish_name not in dish_names:
        return abort(404)

    d_name = build_dict(data['Recipes'], key="Name")
    dish_info = d_name.get(dish_name)
    dish_info_image = f"images/{dish_info['Image']}"

    return render_template('dish.html', data=data, dish_info=dish_info,
        dish_info_image=dish_info_image)