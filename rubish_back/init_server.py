from flask_script import Manager, Shell
from app import app
from app.database.mysql import db
from flask_migrate import Migrate, MigrateCommand

from flask import _app_ctx_stack

manager = Manager(app)
migrate = Migrate(app, db)


def create_all():
    db.drop_all()
    db.create_all()


def insert_admin():
    from app.dao.user import User, Role
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
