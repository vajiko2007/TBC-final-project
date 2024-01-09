from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, RadioField, DateField
from wtforms.validators import DataRequired, equal_to


class AddProductForm(FlaskForm):
    name = StringField("პროდუქტის სახელი", validators=[DataRequired(message="სახელის ველი სავალდებულოა")])
    price = IntegerField("ფასი", validators=[DataRequired(message="ფასის ველი სავალდებულოა")])
    img = FileField("სურათი",
                    validators=[FileRequired(), FileAllowed(["jpg", "png"], message="მხოლოდ jpg,png ფაილები")])
    category = RadioField("მონიშნეთ კატეგორია", choices=[(1, "ბავშვი"), (2, "კაცი"), (3, "ქალი")])
    submit = SubmitField("დამატება")


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანეთ მომხმარებლის სახელი",
                           validators=[DataRequired(message="სახელის ველი სავალდებულოა")])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired(message="პაროლის ველი სავალდებულოა")])
    repeat_password = PasswordField("გაიმეორეთ პაროლი",
                                    validators=[equal_to("password", message="პაროლები არ ემთხვევა")])
    gender = RadioField("მონიშნეთ სქესი", choices=[("კაცი", "კაცი"), ("ქალი", "ქალი")])
    birthday = DateField("დაბადების თარიღი", validators=[DataRequired(message="ეს ველი სავალდებულოა")])

    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ მომხმარებლის სახელი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired()])
    submit = SubmitField("შესვლა")
