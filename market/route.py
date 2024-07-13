from market import app
from flask import render_template,redirect, url_for,flash,get_flashed_messages,request
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from market import db
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method=="POST":
        #purchased Item
        purchased_item=request.form.get('purchased_item')
        p_item_obj=Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f"Congratulation! You purchased {p_item_obj.name} for {p_item_obj.price}",category='success')
            else:
                flash(f"Opps! You don't have enoug money to purchase {p_item_obj.name}",category='danger')    
       
        #sell Item Logic
        sold_item=request.form.get('sold_item')
        s_item_object=Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulation! You purchased {s_item_object.name} back to market",category='success')
            else:
                flash(f"Someting went wrong with selling {s_item_object.name}",category='danger')    
       



        return redirect(url_for('market_page'))            
    if request.method=="GET":
        items = Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items,purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        temp=User(username=form.username.data,
                             email_address=form.email_address.data,
                             password=form.password1.data)
        db.session.add(temp)
        db.session.commit()
        login_user(temp)
        flash(f"Account Created Successfully! You are now logged in as {temp.username}",category='success')
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


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!",category='info')
    return redirect(url_for('home_page'))

