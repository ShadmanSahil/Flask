from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


#configs 

app=Flask(__name__)

db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

bcrypt=Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def User(user_id):
    return User.query.get(user_id)


#forms

class RegisterForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(message='This cannot be empty')])
    email=StringField('Email', validators=[DataRequired(message='This cannot be empty'), Email(message='Enter a valid email')])
    password=PasswordField('Password', validators=[DataRequired(message='This cannot be empty')])
    confirm=PasswordField('Confirm Password', validators=[DataRequired(message='This cannot be empty'), EqualTo(password, message='Passwords do not match')])
    submit=SubmitField('Register')
    
class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(message='This cannot be empty'), Email(message='Enter a valid email')])
    password=PasswordField('Password', validators=[DataRequired(message='This cannot be empty')])
    submit=SubmitField('Login')

class ComposeForm(FlaskForm):
    receiver=StringField('To:', validators=[DataRequired(message='This cannot be empty')])
    subject=StringField('Subject:')
    content=TextAreaField('Content:', validators=[DataRequired(message='This cannot be empty')])
    send=SubmitField('Send')

#models

class User(db.Model, UserMixin):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(30), nullable=False, unique=True)
    password=db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "User({}, {}, {})".format(self.username, self.email, self.id)

    
#routes

@app.route('/register', methods=['GET','POST'])
def register():
    form=RegisterForm()
    if request.method=='GET':
        return render_template('register.html', form=form)
    email=form.email.data
    check=User.query.filter_by(email=email).first()
    if not check:
        password=bcrypt.generate_password_hash(form.password.data)
        user=User(username=form.username.data, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    flash('This email has already been taken')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if request.method=='GET':
        return render_template('login.html', form=form)
    email=form.email.data
    user=User.query.filter_by(email=email).first()
    if user:
        password=form.password.data
        check=bcrypt.check_password_hash(user.password, password)
        if check:
            flash('You have successfully logged in!')
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Incorrect password')
            return render_template('login.html', form=form)
    flash('No user under this email. Please register.')
    return redirect(url_for('register'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    form=ComposeForm()
    if request.method=='GET':
        return render_template('compose.html', form=form)


if __name__=='__main__':
    app.run(debug=True)
