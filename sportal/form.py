from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError
from sportal.models import User, Course
from flask_login import current_user

# For Course Form Select Field
all_courses = Course.query.all()
choices = [('','-- Courses --')]
for course in all_courses:
    a = (course.course_name, course.course_name)
    choices.append(a)


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist!')

    def validate_email(self, email_to_check):
        email_add = User.query.filter_by(email=email_to_check.data).first()
        if email_add:
            raise ValidationError('Email Address already exist!')

    fname = StringField(label='First Name', validators=[Length(min=3, max=30), DataRequired()])
    lname = StringField(label='Last Name', validators=[Length(min=3, max=30), DataRequired()])
    username = StringField(label='Username', validators=[Length(min=5, max=15), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6, max=18), DataRequired()])
    gender = SelectField(label='Gender', choices=[('','-- Gender --'), ('Male','Male'), ('Female','Female')], validators=[DataRequired()])
    submit = SubmitField(label='Register')

class UpdateProfile(FlaskForm):
    fname = StringField(label='First Name', validators=[Length(min=3, max=30), DataRequired()])
    lname = StringField(label='Last Name', validators=[Length(min=3, max=30), DataRequired()])
    gender = SelectField(label='Gender', choices=[('','-- Gender --'), ('Male','Male'), ('Female','Female')], validators=[DataRequired()])
    submit = SubmitField(label='Update')

class UpdateAccount(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            if user != current_user:
                raise ValidationError('Username is already taken!')

    def validate_email(self, email_to_check):
        email_add = User.query.filter_by(email=email_to_check.data).first()
        if email_add:
            if email_add != current_user:
                raise ValidationError('Email Address not avaliable!')

    username = StringField(label='Username', validators=[Length(min=5, max=15), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Update')

class UpdatePassword(FlaskForm):
    curr_pass = PasswordField(label='Current Password', validators=[DataRequired()])
    new_pass = PasswordField(label='New Password', validators=[Length(min=6, max=18), DataRequired()])
    con_new_pass = PasswordField(label='Confirm New Password', validators=[EqualTo('new_pass', message="Password don't match!")])
    submit = SubmitField(label='Change Password')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

# class AdminLogin(FlaskForm):
#     username = StringField(label='Username', validators=[DataRequired()])
#     password = PasswordField(label='Password', validators=[DataRequired()])
#     submit = SubmitField(label='Sign In')

class EnrollForm(FlaskForm):
    courses = SelectField(label='Avaliable Courses', choices=choices, validators=[DataRequired()])
    submit = SubmitField(label='ENROLL')

class UnenrollForm(FlaskForm):
    submit = SubmitField(label='Yes! UNENROLL')

