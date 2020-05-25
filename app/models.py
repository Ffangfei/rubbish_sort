from app import db
from datetime import datetime


class Role:
    ROLE_USER = 0
    ROLE_ADMIN = 1


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    role = db.Column(db.SmallInteger, default=Role.ROLE_USER)
    rubs = db.relationship('Rubbish', backref='author', lazy='dynamic')
    # punishs = db.relationship('Punish',backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_role_id(self):
        return self.role

    def __repr__(self):
        return '<User %r>' % (self.username)

    @classmethod
    def login_check(cls, username, password):
        user = cls.query.filter(db.and_(User.username == username, User.password == password)).first()
        if not user:
            return None
        return user


class Rubbish(db.Model):
    __tablename__ = 'rubbishs'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    weight = db.Column(db.Integer)
    community = db.Column(db.String(100))
    time = db.Column(db.DateTime,
                     default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Punish(db.Model):
    __tablename__ = 'punishs'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64))
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    message = db.Column(db.String(100))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user = db.Column(db.String(64), unique=True)
