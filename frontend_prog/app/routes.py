from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        preferences = request.form.get('preferences')
        print(f"Student: {student_name} | Preferences: {preferences}")
    return render_template('students.html')

@main.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if request.method == 'POST':
        meeting_title = request.form.get('meeting_title')
        meeting_date = request.form.get('meeting_date')
        meeting_time = request.form.get('meeting_time')
        meeting_description = request.form.get('meeting_description')
        print(f"Meeting Created: {meeting_title} on {meeting_date} at {meeting_time}")
    return render_template('teachers.html')
