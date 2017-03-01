from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import Required, Email

class InputForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    upload_file = FileField('Upload', validators=[FileRequired()])
    submit = SubmitField('Submit')