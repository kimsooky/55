from flask import Blueprint, render_template
from models import Students


dev_name = Blueprint('dev_name', __name__)

@dev_name.route('/dev')
def developer():
    students = Students.query.all()
    return render_template("dev.html", students=students)