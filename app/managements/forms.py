from flask_wtf import FlaskForm
# from wtforms.fields import SearchField
from wtforms.fields.html5 import SearchField
from wtforms import StringField, SubmitField, SelectField, DecimalField, TextAreaField
from wtforms.validators import ValidationError, DataRequired
from app.models import Product

class ManagerForm(FlaskForm):
    product_categories = [('Fruit'), ('Vegetable'), ('Canned'), ('Bread'),
        ('Grain'), ('Drink'), ('Snack'), ('Condiment'), ('Protien'),
        ('Baby Products'), ('Dairy'), ('Cooking Oil')]
    package_list = [('Single'), ('Bag'), ('Box'), ('Case'), ('Bottle'),
        ('Packet'), ('Carton'), ('Gallon')]
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_type = SelectField(u'Type', choices=product_categories)
    package_type = SelectField(u'Package Type', choices=package_list)
    quantity = DecimalField('Quantity')
    max_quantity = DecimalField('Max Quantity')
    min_quantity = DecimalField('Min Quantity')

    def validate_product_name(self, product_name):
        product = Product.query.filter_by(product_name=product_name.data.title()).first()

        if product is not None:
            raise ValidationError('Given product already exists!.')


class UpdateProductForm(ManagerForm):
    pass

    def validate_product_name(self, product_name):
        pass


class UpdateQuantityForm(FlaskForm):
    quantity = SelectField(u'Quantity', choices=[x for x in range(0, 11)])


class SearchForm(FlaskForm):
    search_product = SearchField('Search', validators=[DataRequired()])


class EraseProductsForm(FlaskForm):
    submit = SubmitField('Erase')