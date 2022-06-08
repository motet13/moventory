from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login, ma
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.body}>'


# class FeedbackSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Feedback


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), unique=True)
    product_type = db.Column(db.String(120))
    package_type = db.Column(db.String(120))
    quantity = db.Column(db.Float)
    min_quantity = db.Column(db.Float)
    max_quantity = db.Column(db.Float)

    def __repr__(self):
        return f'<Product {self.product_name}, {self.product_type}, {self.package_type}, {self.quantity}, {self.min_quantity} ,{self.max_quantity}>'

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
