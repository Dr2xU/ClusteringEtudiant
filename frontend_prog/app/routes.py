from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/students')
def students():
    return render_template('students.html')

@main.route('/teachers')
def teachers():
    return render_template('teachers.html')
