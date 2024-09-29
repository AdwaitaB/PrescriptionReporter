from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import random
import secrets
import json
from flask_login import login_user, current_user
from .prescriber import Prescriber
from .patient import Patient
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/prescriber/login')
def login():
    return render_template("prescriberlogin.html")

@auth.route('/prescriber/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Prescriber.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/prescriber/signup')
def signup():
    return render_template("prescribersignup.html")

@auth.route('/prescriber/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = Prescriber.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = Prescriber(email=email, name=name, password=generate_password_hash(password), id=random.randint(0,15000000))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/createPatient', methods=['POST'])
def createPatient():
    patient = {}
    patient["name"] = request.form.get('patient-name')
    patient["age"] = request.form.get('patient-age')
    patient["gender"] = request.form.get('patient-gender')
    patient["severity"] = request.form.get('patient-severity')
    patient["records"] = request.form.get('patient-records')
    patient["history"] = request.form.get('patient-medicine')
    patient["family"] = request.form.get('patient-family-history')
    patient["bloodtype"] = request.form.get('patient-blood-type')
    patient["id"] = random.randint(0,15000000)

    with open("data/patients/" + str(patient["id"]) + ".json", "w+") as f:
        json.dump(patient, f)

    code = ""

    with open("data/currentCreate.json", "r+") as f:
        currentIds = json.load(f)
        code = secrets.token_urlsafe(64)
        while (code in currentIds):
            code = secrets.token_urlsafe(64)
        currentIds[code] = patient["id"]
    
    with open("data/currentCreate.json", "w") as f:
        json.dump(currentIds, f)
    
    currentClients = []
    with open("data/prescribers/" + str(current_user.id) + ".json", "r") as f:
        currentClients = json.load(f)

    currentClients.append(patient["id"])

    with open("data/prescribers/" + str(current_user.id) + ".json", "w") as f:
        json.dump(currentClients, f)

    return "medhub.compare/patient/new/" + code

@auth.route("/patient/login")
def clientlogin():
    return render_template("patientlogin.html")

@auth.route("/patient/login", methods=["POST"])
def clientlogin_post():
    # login code goes here
    id = request.cookies.get("id")
    password = request.form.get('password')

    user = Patient.query.filter_by(id=id).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.form'))

@auth.route("/patient/new/<creationID>")
def createClient(creationID):
    currentIds = {}
    with open("data/currentCreate.json", "r+") as f:
        currentIds = json.load(f)
    
    userID = currentIds[creationID]

    return render_template("patientregister.html", userID=userID)

@auth.route("/patient/register", methods=["POST"])
def clientregister():
    password = request.form.get('password')
    userID = request.form.get('userID')
    print(password, userID)

    user = Patient.query.filter_by(id=userID).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('.main.index'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = Patient(id=userID, password=generate_password_hash(password))

    with open("data/currentCreate.json", "r+") as f:
        currentIds = json.load(f)


    for x in currentIds:
        if (currentIds[x] == userID):
            del currentIds[x]
            break
    
    with open("data/currentCreate.json", "w") as f:
        json.dump(currentIds, f)
    

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    resp = make_response(redirect(url_for('auth.clientlogin')))
    resp.set_cookie("id",userID)

    return resp

@auth.route('/logout')
def logout():
    return 'Logout'