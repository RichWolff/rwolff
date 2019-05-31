from flask_wtf import Form as FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField,DateField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf, ValidationError
from rwolff.models import User

class projectForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextField('Project Description', validators=[DataRequired()])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    active_state = RadioField('Project Display State', choices = [('Active','Active'), ('Preview','Preview'), ('Disable','Disable')])
    submit = SubmitField('Submit Project')

class postForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    active_state = RadioField('Project Display State', choices = [('Active','Active'), ('Preview','Preview'), ('Disable','Disable')])
    submit = SubmitField('Submit Post')

class projectDetailsForm(FlaskForm):
    attr = StringField('Project Attribute', validators=[DataRequired(),AnyOf(['Tag','Collaborator','Detail']), Length(min=2, max=20)])
    value = TextField('Value',validators=[DataRequired()])
    sumbit = SubmitField('Add')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Exists. Please login with your existing email')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    nickname = StringField('Nickname')
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update Account')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Already Exists. Please login with your existing email')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
