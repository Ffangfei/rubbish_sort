from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

def create_all():
    db.drop_all()
    db.create_all()


def insert_admin():
    from app.models import User, Role
    user = User()
    user.role = Role.ROLE_ADMIN
    user.username = 'admin'
    user.password = 'root'
    user.about_me = 'i am admin'
    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


if __name__ == '__main__':
    create_all()
    insert_admin()
