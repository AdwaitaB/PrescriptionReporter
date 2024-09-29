from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import medication as med
import json
from . import db

main = Blueprint('main', __name__)

@main.route('/prescriber/dashboard')
def profile():
    id = current_user.id
    with open("data/prescribers/" + str(id) + ".json", "r") as f:
        patients = json.load(f)
    data = []
    for x in patients:
        with open("data/patients/" + str(x) + ".json", "r") as f:
            data.append(json.load(f))
    
    return render_template("prescriber.html", patientInfo=data)

@main.route("/patient")
def form():
    id = current_user.id
    with open("data/patients/" + str(id) + ".json", "r") as f:
        meds = json.load(f)["history"]
    questions = med.medication().getMedication(meds).getQuestions()
    return render_template("patient.html", questions=questions)

