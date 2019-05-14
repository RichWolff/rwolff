from flask_wtf import Form as FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf

class projectForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=20)])
    description = TextField('Project Description', validators=[DataRequired()])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    submit = SubmitField('Submit Project')

class projectDetailsForm(FlaskForm):
    attr = StringField('Project Attribute', validators=[DataRequired(),AnyOf(['Tag','Collaborator','Detail']), Length(min=2, max=20)])
    value = TextField('Value',validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class projectHeader(FlaskForm):
    title = StringField('Email',
                        validators=[DataRequired(), Email()])
    description = PasswordField('Password', validators=[DataRequired()])
