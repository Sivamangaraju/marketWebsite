from market import app
from flask import render_template,redirect, url_for,flash,get_flashed_messages
from market.models import Item,User
from market.forms import RegisterForm,LoginForm
from market import db
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        temp=User(username=form.username.data,
                             email_address=form.email_address.data,
                             password=form.password1.data)
        db.session.add(temp)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors !={}: # check if the all the validation satisfies or not
        for err in form.errors.values():
            flash(f"Opps Some Error Occur, Please Enter Details Correctly🤷‍♂️ {err}",category='danger')
    
    return render_template('register.html',form=form)



@app.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        temp_user=User.query.filter_by(username=form.username.data).first()
        if temp_user and temp_user.passwordCorrection(userPass=form.password.data):
            login_user(temp_user)
            flash(f'Success! You are Logged in as:{temp_user.username }',category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password are not match! Please try again',category='danger')


    return render_template('login.html',form=form)
