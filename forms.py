from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , DateTimeField ,SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateTimeLocalField , DateField


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    birthday =DateField('mm/dd/yyyy', format='%Y-%m-%d', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    birthday =DateField('mm/dd/yyyy', format='%Y-%m-%d', validators=[DataRequired()])

class SearchForm(FlaskForm):
    search = StringField('search' , validators=[DataRequired()])
    submit = SubmitField('submit')

