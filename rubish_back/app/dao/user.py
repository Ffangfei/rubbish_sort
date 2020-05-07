from app.database.mysql import db
from flask_login import UserMixin, AnonymousUserMixin, current_user
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query, count_query, page_query
from app.utils.error import CustomError
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from itsdangerous import URLSafeSerializer
from enum import Enum


class Role(Enum):
    ROLE_ADMIN = 0
    ROLE_USER = 1


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   index=True)
    username = db.Column(db.String(64), index=True, default='')
    password_hash = db.Column(db.String(128), default='')
    community = db.Column(db.String(128), default='')
    role = db.Column(db.SmallInteger, default=Role.ROLE_USER)
    about_me = db.Column(db.Text, default='')
    last_seen = db.Column(db.DateTime, default=datetime.now)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, user):  # 格式化数据
        if user is None:
            return None
        user_dict = {
            'id': user.id,
            'username': user.username,
            'password_hash': user.password_hash,
            'community': user.community,
            'role': user.role,
            'about_me': user.about_me,
            'last_seen': user.last_seen,
            'using': user.using
        }
        return user_dict

    @classmethod
    def reformatter_update(cls, data: dict):  # 格式化更新数据
        allow_change_list = ['password', 'about_me', 'last_seen', 'community']
        update_data = dict()
        for key, value in data.items():
            if key in allow_change_list:
                update_data[key] = value
        return update_data

    @classmethod
    def reformatter_insert(cls, data: dict):  # 格式化插入数据
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):  # 用户查询数量
        if query_dict is None:
            query_dict = {}
        query = User.query
        if not unscoped:
            query = query.filter(User.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, User)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @property
    def password(self):  # 获取哈希后的用户密码
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # 获取用户密码
        self.password_hash = generate_password_hash(password)  #将密码hash加密

    @classmethod
    def get_user(cls, query_dict: dict, unscoped=False):  # 获取用户
        user = User.query
        if not unscoped:
            user = user.filter(User.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            user = process_query(user, url_condition.filter_dict,
                                 url_condition.sort_limit_dict, User).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(user)

    @classmethod
    def query_users(cls, query_dict: dict = None, unscoped=False):  # 获取用户列表
        if query_dict is None:
            query_dict = {}
        query = User.query
        if not unscoped:
            query = query.filter(User.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict,
                                  url_condition.sort_limit_dict, User)
            (users, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(user) for user in users], total

    @classmethod
    def insert_user(cls,  data=None):  # 插入用户
        if data is None:
            raise CustomError(500, 200, 'data must be given')
        data = cls.reformatter_insert(data)
        user = User()
        for key, value in data.items():
            if key == 'password':
                user.password = value
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.add(user)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_user(cls,  username: str = None):  # 删除用户
        try:
            user = User.query.filter(User.username == username).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        user.using = False
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_user(cls, username: str = None, data: dict = None):  # 更新用户
        if data is None:
            data = {}
        data = cls.reformatter_update(data)
        try:
            user = User.query.filter(User.username == username).filter(
                User.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for key, value in data.items():
            if hasattr(user, key) or key == 'password':
                setattr(user, key, value)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CustomError(500, 500, str(e))

        return True
