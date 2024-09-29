from flask import Blueprint, render_template
from flask_login import login_required, current_user
import json
from . import db

main = Blueprint('main', __name__)

@main.route('/prescriber/dashboard')
@login_required
def profile():
    id = current_user.id
    with open("data/prescribers/" + str(id) + ".json", "r") as f:
        patients = json.load(f)
    data = []
    for x in patients:
        with open("data/patients/" + str(x) + ".json", "r") as f:
            data.append(json.load(f))
    
    return render_template("prescriber.html", patientInfo=data)