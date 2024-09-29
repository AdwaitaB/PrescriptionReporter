from flask import Blueprint, render_template
from flask_login import login_required
from . import db

main = Blueprint('main', __name__)

@main.route('/prescriber/dashboard')
@login_required
def profile():
    return render_template("prescriber.html")