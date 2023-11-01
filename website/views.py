from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . models import Note, Requests
from . import db
import json
from sqlalchemy.sql import func
from sqlalchemy import engine, text
from .models import User, Note, Requests, Family,Log, Activity

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if (request.method=='POST'):
        note=request.form.get('note')
        if (len(note)<1):
            flash('Note is too short!', category='error')
        else:
            new_note=Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if (note):
        if(note.user_id==current_user.id):
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/resident-home', methods=['GET','POST'])
@login_required
def residentHome():
    res = db.session.execute(text('select email from Log where Log.id=:id'), {'id': current_user.id})
    email = res.fetchone()[0] 
    user = User.query.filter_by(email=email).first()
    return render_template('/residentHome.html', user=user, role="resident")

@views.route('/resident-request', methods=['GET','POST'])
@login_required
def residentRequest():
    if (request.method=='POST'):
        userRequest=request.form.get('userRequest')
        if (len(userRequest)<1):
            flash('Request is too short!', category='error')
        else:
            new_userRequest=Requests(userRequest=userRequest, user_id=current_user.id)
            db.session.add(new_userRequest)
            db.session.commit()
            flash('Request Registed!', category='success')
    res = db.session.execute(text('select email from Log where Log.id=:id'), {'id': current_user.id})
    email = res.fetchone()[0]  # Using fetchone() because we expect at most one result
    # user = db.session.execute(text('select * from User where email=:email'),{'email':email})
    # current_user = user.fetchone()[0]
    # print(current_user)
    print(email)
    user = User.query.filter_by(email=email).first()
    print(user)
    return render_template("resident.html", user=user, role="resident")


@views.route('/resident-activity', methods=['GET','POST'])
@login_required
def residentActivity():
    if (request.method=='POST'):
        userActivity=request.form.get('activity')
        date=request.form.get('date1')
        if (len(userActivity)<1):
            flash('Activity is too short!', category='error')
        else:
            new_userActivity=Activity(activity=userActivity, user_id=current_user.id, date=date)
            db.session.add(new_userActivity)
            db.session.commit()
            flash('Activity Registed!', category='success')
    res = db.session.execute(text('select email from Log where Log.id=:id'), {'id': current_user.id})
    email = res.fetchone()[0]  # Using fetchone() because we expect at most one result
    # user = db.session.execute(text('select * from User where email=:email'),{'email':email})
    # current_user = user.fetchone()[0]
    # print(current_user)
    print(email)
    user = User.query.filter_by(email=email).first()
    print(user)
    return render_template("activity.html", user=user, role="resident")


@views.route('/delete-activity', methods=['POST'])
def delete_activity():
    delActivity=json.loads(request.data)
    activityId=delActivity['activityId']
    delActivity=Activity.query.get(activityId)
    if (delActivity):
        if(delActivity.user_id==current_user.id):
            db.session.delete(delActivity)
            db.session.commit()
    return jsonify({})


@views.route('/delete-request', methods=['POST'])
def delete_request():
    delRequest=json.loads(request.data)
    requestId=delRequest['requestId']
    delRequest=Requests.query.get(requestId)
    if (delRequest):
        if(delRequest.user_id==current_user.id):
            delRequest.status="past"
            db.session.commit()
    return jsonify({})



@views.route('/family-home', methods=['GET','POST'])
@login_required
def familyHome():
    print(current_user.name)
    res = db.session.execute(text('select email from Log where Log.id=:id'), {'id': current_user.id})
    email = res.fetchone()[0] 
    user = Family.query.filter_by(email=email).first()
    print(user.name, user.resident_name)
    print(user)
    requests=db.session.execute(text("select userRequest from Requests where Requests.user_id=:id and status = 'active'"), {'id': user.residentId}).fetchall()
    print(requests)
    activities=db.session.execute(text("select activity, date from Activity where Activity.user_id=:id"), {'id': user.residentId}).fetchall()
    print(activities)
    return render_template("familyHome.html", user=user, role="family", requests=requests, activities=activities)