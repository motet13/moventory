from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, TextAreaField
from wtforms.validators import ValidationError, DataRequired
from flask_wtf.file import FileField, FileAllowed

class RecipeForm(FlaskForm):
    # dish_name = StringField('Dish Name', validators=[DataRequired()])
    # dish_description = TextAreaField('Description', validators=[DataRequired()])
    # dish_ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    # dish_instructions = TextAreaField('Instructions', validators=[DataRequired()])
    # dish_image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    # submit = SubmitField('Create Recipe')

    # TESTING
    dish_name = StringField('Dish Name', validators=[DataRequired()])
    dish_description = TextAreaField('Description', validators=[DataRequired()])
    dish_ingredient_whole_measurements = SelectField(u'measurements', choices=[('', ''), ('1', '1'), ('2', '2'), ('3', '3')])
    dish_ingredient_fraction_measurements = SelectField(u'measurements', choices=[('', ''), ('1/2', '1/2'), ('1/4', '1/4'), ('1/8', '1/8')])
    dish_measurement_type = StringField('Type', validators=[DataRequired()])
    dish_ingredient_name = StringField('Ingredient', validators=[DataRequired()])
    dish_instructions = TextAreaField('Instructions', validators=[DataRequired()])
    dish_image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Create Recipe')



    # def validate_product_name(self, product_name):
    #     product = Product.query.filter_by(product_name=product_name.data.title()).first()

    #     if product is not None:
    #         raise ValidationError('Given product already exists!.')