from flask import render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from models import Product, User, Wishlist
from forms import AddProductForm, RegisterForm, LoginForm
from ext import app, db


@app.route("/")
def index():
    all_products = Product.query.limit(12).all()
    return render_template("main.html", products=all_products)


@app.route("/product/<int:product_id>")
def view_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")
    return render_template("product.html", chosen_product=chosen_product)


@app.route("/add_product", methods=["POST", "GET"])
@login_required
def add_product():
    if current_user.role != "admin":
        return redirect("/")

    form = AddProductForm()
    print(app.root_path + '/static')

    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data, img=form.img.data.filename,
                              category_id=form.category.data)
        db.session.add(new_product)
        db.session.commit()

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)

        return redirect("/")
    return render_template("add_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    if current_user.role != "admin":
        return redirect("/")

    form = AddProductForm(name=chosen_product.name, price=chosen_product.price, img=chosen_product.img)
    if form.validate_on_submit():
        chosen_product.name = form.name.data
        chosen_product.price = form.price.data
        chosen_product.img = form.img.data.filename

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)

        db.session.commit()

    return render_template("add_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    if current_user.role != "admin":
        return redirect("/")

    db.session.delete(chosen_product)
    db.session.commit()
    return redirect("/")


@app.route("/wish_list")
@login_required
def wish_list():
    user_wishlist = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template("wish_list.html", user_wishlist=user_wishlist)


@app.route("/add_to_wish_list/<int:product_id>", methods=["POST", "GET"])
@login_required
def add_to_wish_list(product_id):
    if Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        flash("Product already in your wish list!")
    else:
        chosen_product = Product.query.get(product_id)
        if chosen_product:
            new_wishlist_item = Wishlist(
                user_id=current_user.id,
                product_id=chosen_product.id,
                product_img=chosen_product.img,
                price=chosen_product.price
            )
            db.session.add(new_wishlist_item)
            db.session.commit()

    return redirect("/")


@app.route("/delete_wish_list_product/<int:wishlist_item_id>")
@login_required
def delete_wish_list_product(wishlist_item_id):
    wishlist_item = Wishlist.query.get(wishlist_item_id)

    if not wishlist_item:
        return render_template("404.html")

    db.session.delete(wishlist_item)
    db.session.commit()

    return redirect(url_for("wish_list"))


@app.route("/category/<int:category_id>")
def category(category_id):
    products = Product.query.filter(Product.category_id == category_id).all()
    return render_template("catalog.html", products=products)


@app.route("/search/<string:name>")
def search(name):
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template("search.html", products=products)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("თქვენ მიერ ჩაწერილი სახელი უკვე გამოყენებულია ცადეთ სხვა")
        else:
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        flash("Invalid username or password", "error")
        if user and user.check_password(form.password.data):
            login_user(user)
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
