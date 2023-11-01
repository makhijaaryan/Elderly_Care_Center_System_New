from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import User, Family, Log
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if(request.method=='POST'):
        email = request.form.get('email')
        password=request.form.get('password1')
        user=Log.query.filter_by(email=email).first()
        login_user(user, remember=True)
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                print(user.role)
                if(user.role=="resident"):
                    user=User.query.filter_by(email=email).first()
                    # login_user(user, remember=True)
                    print(user.name)
                    return redirect(url_for('views.residentHome'))
                elif(user.role=="family"):    
                    print(user.email)                
                    user=Family.query.filter_by(email=email).first()
                    print(user.name)
                    print(user.role)
                    # login_user(user, remember=True)
                    return redirect(url_for('views.familyHome'))   
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exists.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/signup', methods= ['GET', 'POST'])
def signup():
    if request.method == "POST":
        # id=request.form.get('id')
        email=request.form.get('email')
        name=request.form.get('name')
        pass1=request.form.get('password1')
        pass2=request.form.get('password2')
        contactNo=request.form.get('contactNo')
        role=request.form.get('role')

        user=Log.query.filter_by(email=email).first()
        
        if(user):
            flash('User already exists!', category='error')
        elif(pass1!=pass2):
            flash("Passwords must match!", category='error')
        elif (len(contactNo)!=10):
            flash("Incorrect number entered!", category='error')
        else:
            new_log=Log(name=name,email=email, password=generate_password_hash(pass1,method='sha256'), role=role)
            # new_user=User(email=email, name=name, password=password, contactNo=contactNo)
            new_user=User(email=email, name=name, contactNo=contactNo, role=role)
            db.session.add(new_log)
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)
            flash("Account created!", category='success')
            print(f"Name:{name}\nEmail:{email}\nPassword: {pass1}\nContact Number:{contactNo}\nRole:{role}\n")
            return redirect(url_for('auth.login'))
         
    return render_template("signup.html", user=current_user)

@auth.route('/registerFamily', methods= ['GET', 'POST'])
def registerFamily():
    if request.method == "POST":
        resident_id=current_user.id
        email=request.form.get('email')
        name=request.form.get('name')
        pass1=request.form.get('password1')
        pass2=request.form.get('password2')
        contactNo=request.form.get('contactNo')
        role='family'
        resident_name=current_user.name
        
        user=Family.query.filter_by(email=email).first()
        if(user):
            flash('User already exists!', category='error')
        elif(pass1!=pass2):
            flash("Passwords must match!", category='error')
        elif (len(contactNo)!=10):
            flash("Incorrect number entered!", category='error')
        else:
            password=generate_password_hash(pass1,method='sha256')
            new_log=Log(name=name, email=email,password=password, role=role)
            db.session.add(new_log)
            new_Famliy=Family(residentId=resident_id,email=email, name=name, contactNo=contactNo, resident_name=resident_name, role=role)
            # new_Famliy=Family(residentId=resident_id,email=email, name=name, password=password, contactNo=contactNo, resident_name=resident_name)
            db.session.add(new_Famliy)
            db.session.commit()
            flash("Family member registered!", category='success')
            print(f"Resident id: {resident_id}\nName:{name}\nEmail:{email}\nPassword: {pass1}\nContact Number:{contactNo}\nResident Name: {resident_name}\n")
            return redirect(url_for('views.residentHome'))
    return render_template("registerFamily.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))