import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from app.models import Group, GroupMember, StudentVote, Student, Election

def clean_database():
    print("Deleting GroupMembers...")
    GroupMember.query.delete()
    db.session.commit()

    print("Deleting Groups...")
    Group.query.delete()
    db.session.commit()

    print("Deleting StudentVotes...")
    StudentVote.query.delete()
    db.session.commit()

    print("Deleting Elections...")
    Election.query.delete()
    db.session.commit()

    # Uncomment below if you want to delete all students (use with caution!)
    print("Deleting Students...")
    Student.query.delete()
    db.session.commit()

    print("Database cleanup completed.")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        clean_database()
