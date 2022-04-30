from flask import render_template, flash, request, jsonify, make_response
from flask.helpers import url_for
import requests
from werkzeug.utils import redirect
from app import db 
from flask_login import current_user, login_required
from app.models import Product, ProductSchema
from app.utils import total_recipes, total_task
from datetime import date, datetime
from flask import Blueprint
from config import Config
from app.main.forms import SchedulerForm
import csv
from os.path import exists

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    tday = date.today().strftime("%A, %m-%d-%Y")
    products = Product.query.order_by(Product.product_name).all()
    num_items = len(products)
    recipe_counts = total_recipes()
    activate_gen = 'false'
    task_counts = total_task()

    for product in products:
        if product.quantity <= product.min_quantity:
            activate_gen = 'true'
            break

    user = current_user

    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products) 
    res = make_response(jsonify(output), 200)

    return render_template('index.html', title='MoVintory', products=products,
        tday=tday, num_items=num_items, res=res.get_json(), user=user,
        activate_gen=activate_gen, recipe_counts=recipe_counts,
        task_counts=task_counts)


@main.route('/quantity-entry', methods=['POST'])
def quantity_entry():
    req = request.get_json()
    product = Product.query.filter_by(product_name=req.get('prod_name').title()).first()
    product.quantity = req.get('qty_value')
    product_schema = ProductSchema()
    output = product_schema.dump(product)
    db.session.commit()
    res = make_response(jsonify(output), 200)

    return res


@main.route('/search-entry', methods=['POST'])
def search_entry():
    req = request.get_json()
    product = Product.query.filter_by(product_name=req.get('search').title()).first()
    product_schema = ProductSchema()
    output = product_schema.dump(product) 

    if product is not None: 
        res = make_response(jsonify(output), 200)
    else:
        res = make_response(jsonify({"Error": "Product not found"}), 500)

    return res


@main.route('/products', methods=['GET'])
def products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products) 
    res = make_response(jsonify(output), 200)

    return res


@main.route('/index/gen-prod-lists', methods=['GET'])
@login_required
def gen_prod_lists():
    products = Product.query.all()
    # Uncomment lines below after testing
    shopping_list = {"sheet1": []}
    
    for product in products:
        if product.quantity <= product.min_quantity:
            shopping_list["sheet1"].append(
                {
                    "item": product.product_name,
                    "currentQuantity": product.quantity,
                    "boughtQuantity": 0,
                    "movintoryId": product.id
                })

    if len(shopping_list['sheet1']) != 0:
        # POST shopping list to google sheet using sheety API
        sheety_endpoint = Config.SHEETY_ENDPOINT
        sheety_headers = { "Authorization": f"Bearer {Config.MOVINTORY_SHEETY_TOKEN}" }
        
        for item in shopping_list['sheet1']:
            requests.post(sheety_endpoint, json={"sheet1":item}, headers=sheety_headers)        
    else:
        flash(f'You do not need to go shopping yet.', 'info mt-2')
        return redirect(url_for('main.index'))

    res = make_response(jsonify(shopping_list), 200)

    return render_template('generated_lists.html', res=res.get_json())


@main.route('/index/refresh-list', methods=['GET', 'POST'])
def refresh():
    token = Config.MOVINTORY_REFRESH_TOKEN
   
    if request.method == 'POST':
        request_token = request.headers.get('Authorization')
        if request_token == token:
            shopping_list = request.get_json()
            response_data = shopping_list['sheet1']

            for item in response_data:
                product = Product.query.get_or_404(item['movintoryId'])
                product.quantity = int(item['boughtQuantity']) + product.quantity
    
            db.session.commit()

            return "{'response': 'Okay'}"
        return "{'response': 'BAD AUTH'}"
    return "{'response': 'This page is for refreshing your shopping list up to date.'}"


@main.route('/<int:product_id>', methods=['GET', 'POST'])
def quantity(product_id):
    product = Product.query.get_or_404(product_id)
    product_schema = ProductSchema()
    output = product_schema.dump(product) 
    res = make_response(jsonify(output), 200)

    return res

@main.route('/index/schedule_reminder', methods=['GET', 'POST'])
def schedule_reminder():
    form = SchedulerForm()
    schedule_file = f"{Config.MOVINTORY_SCHEDULE_PATH}/schedule.csv"

    if request.method == 'POST':
        title = form.title.data.title()
        date = form.date.data
        message = form.message.data

        try:
            with open(schedule_file, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
        except FileNotFoundError as e:
            with open(schedule_file, 'w', newline='') as new_file:
                fieldnames = ['Subject', 'DueDate', 'Message']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow({'Subject': title, 'DueDate': date, 'Message': message})
        else:
            with open(schedule_file, 'a') as append_csv_file:
                fieldnames = ['Subject', 'DueDate', 'Message']
                csv_writer = csv.DictWriter(append_csv_file, fieldnames=fieldnames)
                csv_writer.writerow({'Subject': title, 'DueDate': date, 'Message': message})

        flash(f'"{title}" has been scheduled!', 'success mt-2')
        return redirect(url_for('main.schedule_reminder'))

    return render_template('reminder.html', form=form)


@main.route('/index/scheduled-list', methods=['GET', 'POST'])
def scheduled_list():
    csv_file = f'{Config.MOVINTORY_SCHEDULE_PATH}/schedule.csv'
    scheduled_list_dict = {"Task": []}
    tday = datetime.now().timestamp()

    if exists(csv_file):
        with open(csv_file, 'r') as file:
            read_csv = csv.DictReader(file)
            for line in read_csv:
                scheduled_list_dict['Task'].append({
                    'Subject': line['Subject'],
                    'DueDate': datetime.fromisoformat(line['DueDate'])
                })

        scheduled_list_dict = sorted(scheduled_list_dict['Task'],
            key=lambda x: x['DueDate'])

    
    return render_template('scheduled_list.html',
        scheduled_list_dict=scheduled_list_dict,
        tday=tday, enumerate=enumerate)


@main.route('/about')
def about():
    user = current_user
    version = 'v2'
    creation_date = 'September 19, 2020'

    return render_template('about.html', title='About', version=version,
        creation_date=creation_date, user=user)