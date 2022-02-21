from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def init_app(app, app_secret_key):
    app.config["SECRET_KEY"] = app_secret_key

    csrf.init_app(app)


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
