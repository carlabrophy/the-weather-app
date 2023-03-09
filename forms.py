from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, DateTimeField, SelectField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class WeatherForm(FlaskForm):

    column = SelectField('Choose which table:', choices=[('left', 'Left'), ('right', 'Right')])
    location = StringField('Location', render_kw={'placeholder': 'newyork'},validators=[InputRequired()])
    date = StringField('Date', render_kw={'placeholder': '03-31'})