import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv
from app.services.admin_service import create_admin
from app.services.teacher_service import create_teacher
from app.services.student_service import create_student
from flask import jsonify
load_dotenv()

from flask import redirect
from app.extensions import db  # SQLAlchemy instance
from app.config import Config  # App configuration
from app.models import Admin, Teacher, Student, StudentVote, Election, Group, GroupMember  # Ensure models are imported for table creation

from app import create_app

def main():
    app = create_app()

    @app.route('/routes')
    def list_routes():
        import urllib
        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            line = urllib.parse.unquote(f"{rule.endpoint}: {rule} [{methods}]")
            output.append(line)
        return "<br>".join(sorted(output))

    @app.route('/create_admin')
    def create_admin_route():
        email = "admin@jwc.com"
        password = "admin123"
        try:
            create_admin(email=email, password=password, first_name="Admin", last_name="User")
        except Exception as e:
            return jsonify({"error": f"Failed to create admin: {str(e)}"}), 500
        return jsonify({"message": "Admin created", "email": email, "password": password})

    @app.route('/create_teacher')
    def create_teacher_route():
        email = "0000000000@jwc.com"
        password = "teacher123"
        try:
            create_teacher(email=email, password=password, first_name="Teacher", last_name="User", department="Mathematics", unique_id="0000000000")
        except Exception as e:
            return jsonify({"error": f"Failed to create teacher: {str(e)}"}), 500
        return jsonify({"message": "Teacher created", "email": email, "password": password})

    @app.route('/create_student')
    def create_student_route():
        email = "1111111111@jwc.com"
        password = "student123"
        try:
            create_student(email=email, password=password, first_name="Student", last_name="User", class_name= "Class", section="Section", unique_id="1111111111")
        except Exception as e:
            return jsonify({"error": f"Failed to create student: {str(e)}"}), 500
        return jsonify({"message": "Student created", "email": email, "password": password})

    @app.route('/dump_all_data')
    def dump_all_data():
        try:
            admins = [serialize_model(a) for a in Admin.query.all()]
            teachers = [serialize_model(t) for t in Teacher.query.all()]
            students = [serialize_model(s) for s in Student.query.all()]
            elections = [serialize_model(e) for e in Election.query.all()]
            votes = [serialize_model(v) for v in StudentVote.query.all()]
            groups = [serialize_model(g) for g in Group.query.all()]
            group_members = [serialize_model(m) for m in GroupMember.query.all()]

            return jsonify({
                "admins": admins,
                "teachers": teachers,
                "students": students,
                "elections": elections,
                "votes": votes,
                "groups": groups,
                "group_members": group_members
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

def serialize_model(model):
    """Serialize SQLAlchemy model instance into dict"""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}

if __name__ == '__main__':
    app = main()
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode)
