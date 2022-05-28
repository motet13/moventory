from app.managements.utils import admin_only
from flask import render_template, url_for, flash, redirect, request, jsonify, make_response, send_from_directory, abort
from app import db
from app.managements.forms import ManagerForm, UpdateProductForm, EraseProductsForm
from flask_login import current_user, login_required
from app.models import Feedback, Product, ProductSchema, Token
from secrets import token_hex
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import Blueprint
import json
from config import Config
from json.decoder import JSONDecodeError
from app.utils import load_recipes, build_dict, dumps_recipes
import locale
from os import path, remove

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
managements = Blueprint('managements', __name__)

@managements.route('/manager', methods=['GET', 'POST'])
@login_required
@admin_only
def manager():

    user = current_user
    form = ManagerForm()

    if form.validate_on_submit():
        product = Product(product_name=form.product_name.data.title(), product_type=form.product_type.data,
            package_type=form.package_type.data, quantity=form.quantity.data, max_quantity=form.max_quantity.data,
            min_quantity=form.min_quantity.data)
        db.session.add(product)
        db.session.commit()
        flash(f'{form.product_name.data.title()} have been added to the database', 'success mt-2')

    product = Product.query.order_by(Product.product_name).all()
    num_items = len(product)

    return render_template('manager.html', title='Manager', form=form, product=product, num_items=num_items, user=user)


@managements.route('/manager/modify_products', methods=['GET', 'POST'])
@login_required
def modifyProduct():
    user = current_user
    products = Product.query.order_by(Product.product_name).all()
    num_items = len(products)
    return render_template('modify_products.html', title='Product', products=products, num_items=num_items, user=user)


@managements.route('/manager/<int:product_id>')
@login_required
def product(product_id):
    user = current_user
    product = Product.query.get_or_404(product_id)

    return render_template('product.html', title='Product', product=product, user=user)


@managements.route('/manager/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    user = current_user
    product = Product.query.get_or_404(product_id)

    form = UpdateProductForm()

    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.product_type = form.product_type.data
        product.package_type = form.package_type.data
        product.quantity = form.quantity.data
        product.max_quantity = form.max_quantity.data
        db.session.commit()
        flash(f'{product.product_name} has been updated!', 'success')
        return redirect(url_for('managements.manager', product_id=product.id))
    elif request.method == 'GET':
        form.product_name.data = product.product_name
        form.product_type.data = product.product_type
        form.package_type.data = product.package_type

    return render_template('update_product.html', title='Update Product',
        form=form, product=product,user=user)


@managements.route('/manager/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted!', 'success mt-2')
    return redirect(url_for('managements.manager'))


@managements.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    user = current_user
    erase_products_form = EraseProductsForm()

    
    return render_template('settings.html', title='Settings',
        erase_products_form=erase_products_form, user=user)


@managements.route('/settings/erase-products', methods=['POST'])
@login_required
def settings_erase_products():

    erase_products_form = EraseProductsForm()

    if erase_products_form.validate_on_submit():
        products = Product.query.all()
        for product in products:
            db.session.delete(product)
        db.session.commit()
        flash(f'Your invintory is now clean.', 'success mt-2')
        return redirect(url_for('managements.settings'))


@managements.route('/settings/erase-posts', methods=['POST'])
@login_required
def settings_erase_posts():

    erase_feedback_form = EraseFeedbackForm()
    
    if erase_feedback_form.validate_on_submit():
        feedbacks = Feedback.query.all()
        for feedback in feedbacks:
            db.session.delete(feedback)
        db.session.commit()
        flash(f'All posts have been cleared.', 'success mt-2')
        return redirect(url_for('managements.settings'))


@managements.route('/settings/backup-restore', methods=['GET', 'POST'])
@login_required
@admin_only
def settings_backup_restore():
    now = datetime.now()
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)

    if request.method == 'GET':
        backup_file_name = f'ProductsBackup_{now.date()}.json'
        token = token_hex(16)
        new_token = Token(token=token)
        db.session.add(new_token)
        db.session.commit()
        result = {'Token' : token, backup_file_name : {'Products': output}}
        res = make_response(jsonify(result))

        with open(f"{Config.MOVENTORY_DOWNLOAD_FOLDER}/{backup_file_name}", 'w') as file:
            file.write(res.get_data().decode('utf-8'))

        return redirect(url_for('managements.backup_downloads', backup_filename=backup_file_name))

    file = request.files['backupfileToRestore']

    try:
        data = json.loads(file.read())
    except JSONDecodeError:
        flash('No file selected. Please provide a file.', 'danger mt-2')
        return redirect(url_for('managements.manager'))
    else:
        # Save uploaded products json file to server
        is_token = Token.query.filter_by(token=data['Token']).first()
        if file.filename.split('.')[1].lower() == 'json' and is_token is not None:
             # Make a copy of current DB Products and store it for backup.
            original_products_filename = f'original_products_{now.date()}.json'
            with open(f'{Config.MOVENTORY_DB_ORIGINAL_PRODUCT_PATH}/{original_products_filename}', 'w') as original_file:
                original_content = make_response(jsonify({original_products_filename: {'Products': output}}))
                original_file.write(original_content.get_data().decode('utf-8'))

            # Replace the current product data in DB from original to client uploaded product.json
            filename = secure_filename(file.filename)
            file.close()
            file = json.dumps(data, indent=4)
            with open(f"{Config.UPLOAD_FOLDER}/{filename}", 'w') as json_data:
                json_data.write(file)

            uploaded_file = list(data.keys())[0]

            Product.query.delete()
            for product in data[uploaded_file]['Products']:
                new_product = Product(
                    max_quantity=product['max_quantity'],
                    min_quantity=product['min_quantity'],
                    package_type=product['package_type'],
                    product_name=product['product_name'],
                    product_type=product['product_type'],
                    quantity=product['quantity'])
                db.session.add(new_product)
            db.session.commit()

            flash(f'{filename} was successfully uploaded.', 'success mt-2')
            return redirect(url_for('managements.manager'))
        flash('Sorry that is not a valid file.', 'danger mt-2')
        return redirect(url_for('managements.manager'))


@managements.route('/settings/backup-restore/downloads/<backup_filename>')
@login_required
@admin_only
def backup_downloads(backup_filename):
    try:
        return send_from_directory(
            directory=Config.MOVENTORY_DOWNLOAD_FOLDER,
            path=None,
            filename=backup_filename,
            as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

@managements.route('/delete-recipe', methods=['GET', 'POST'])
@login_required
def delete_recipe_dish():
    recipes=load_recipes()

    if request.method == 'POST':
        dish_name = request.get_json()['dish_name']
        d_name = build_dict(recipes['Recipes'], key="Name")
        idx = int(d_name.get(dish_name)['index'])
        image = recipes['Recipes'][idx]['Image']
        image_path = path.join(f"{Config.MOVENTORY_RECIPE_IMAGE_PATH}/" + image)
        if image != 'default.jpg':
            remove(image_path)
        dumps_recipes(data=recipes, dict=None, index=idx, edit=False, delete=True)

    return render_template('delete_recipe.html', recipes=recipes)