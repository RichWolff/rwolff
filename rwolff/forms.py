from flask_wtf import Form as FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField,DateField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf, ValidationError
from rwolff.models import User, Tags

class projectForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextField('Project Description', validators=[DataRequired()])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    active_state = RadioField('Project Display State', choices = [('Active','Active'), ('Preview','Preview'), ('Disable','Disable')])
    submit = SubmitField('Submit Project')

class TagField(StringField):
    def _value(self):
        if self.data:
            # Display tags as a comma-separated list.
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')

        # Filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tags if name.strip()]

        # Query the database and retrieve any tags we have already saved.
        existing_tags = Tags.query.filter(Tags.name.in_(tag_names))

        # Determine which tag names are new.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tags(name=name) for name in new_names]

        # Return all the existing tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

class postForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(min=2, max=100)])
    slug = StringField('Url Slug')
    content = TextAreaField('Content', validators=[DataRequired()])
    active_state = RadioField('Project Display State', choices = [('Active','Active'), ('Preview','Preview'), ('Disable','Disable')])
    post_type = RadioField('Blog Post or Project', choices = [('Blog Post','Blog Post'), ('Project','Project')])
    tags = TagField('Tags')
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
