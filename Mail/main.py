from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField

app=Flask(__name__)

class RegisterForm(FlaskForm):
    username=StringField('Username')
    email=StringField('Email')
    password=PasswordField('Password')
    confirm=PasswordField('Confirm Password')
    submit=SubmitField('Register')

@app.route('/register', methods=['GET','POST'])
def register():
    pass

@app.route('/login', methods=['GET','POST'])
def login():
    pass

if __name__=='__main__':
    app.run(debug=True)
