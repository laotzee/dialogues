from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CommentForm(FlaskForm):

    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):

    name = StringField("Name to be displayed",
                       validators=[
                           DataRequired(),
                       ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired(),
                             ])
    email = EmailField("Email",
                       validators=[
                           DataRequired(),
                       ])
    submit = SubmitField("Submit Post")

class LogInForm(FlaskForm):

    email = EmailField("Email",
                       validators=[
                           DataRequired(),
                       ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired(),
                             ])
    submit = SubmitField("Submit Post")

