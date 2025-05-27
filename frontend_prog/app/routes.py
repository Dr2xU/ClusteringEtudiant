from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/students')
def students():
    if 'user' not in session or session['user']['role'] != 'student':
        return redirect(url_for('main.login'))
    return render_template('students.html')

@main.route('/teachers')
def teachers():
    if 'user' not in session or session['user']['role'] != 'teacher':
        return redirect(url_for('main.login'))
    return render_template('teachers.html')


from flask import Blueprint, render_template, request, redirect, url_for, session
from .db_access import get_user_by_email_password

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email_password(email, password)

        if user:
            session['user'] = {
                'user_id': user[0],
                'email': user[1],
                'role': user[2]
            }

            if user[2] == 'student':
                return redirect(url_for('main.students'))
            elif user[2] == 'teacher':
                return redirect(url_for('main.teachers'))
            else:
                error = "Access denied for this role."
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)
