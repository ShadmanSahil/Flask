from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email

app=Flask(__name__)

class RegisterForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(message='This cannot be empty')])
    email=StringField('Email', validators=[DataRequired(message='This cannot be empty'), Email(message='Enter a valid email')])
    password=PasswordField('Password', validators=[DataRequired(message='This cannot be empty')])
    confirm=PasswordField('Confirm Password', validators=[DataRequired(message='This cannot be empty'), EqualTo(password, message='Passwords do not match')])
    submit=SubmitField('Register')

@app.route('/register', methods=['GET','POST'])
def register():
    pass

@app.route('/login', methods=['GET','POST'])
def login():
    pass

if __name__=='__main__':
    app.run(debug=True)
