from ext import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("product_category.id"))
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    img = db.Column(db.String)

    category = db.relationship("ProductCategory", back_populates="products")


class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    products = db.relationship("Product")


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    wish_list = db.relationship('Wishlist', back_populates='user')

    def __init__(self, username, password, role="normal"):
        self.password = generate_password_hash(password)
        self.username = username
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Wishlist(db.Model):
    __tablename__ = "wish_list"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_img = db.Column(db.String)
    price = db.Column(db.Integer)
    user = db.relationship("User")
    product = db.relationship("Product", back_populates="wishlist")

    def __init__(self, user_id, product_id, product_img, price):
        self.user_id = user_id
        self.product_id = product_id
        self.product_img = product_img
        self.price = price


Product.wishlist = db.relationship("Wishlist", back_populates="product")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        new_user = User("admin", "password", "admin")
        db.session.add(new_user)

        kids_category = ProductCategory(name="kids")
        db.session.add(kids_category)

        man_category = ProductCategory(name="man")
        db.session.add(man_category)

        woman_category = ProductCategory(name="woman")
        db.session.add(woman_category)

        db.session.commit()
