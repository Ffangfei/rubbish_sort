import app.dao as dao
from app.utils import CustomError
from app.database.mysql import db
from flask_login import current_user
from datetime import datetime
from app.utils.error import CustomError


class UserController(object):
    @classmethod
    def formatter(cls, user: dict):  # 格式化用户信息
        new_data = dict()
        for key, value in user.items():
            if key != "password_hash":
                new_data[key] = value
        return new_data

    @classmethod
    def reformatter_insert(cls, data: dict):  # 格式化插入信息
        return data

    @classmethod
    def reformatter_update(cls, data: dict):  # 格式化更新信息
        allow_change_list = ['password', 'about_me', 'last_seen', 'community']
        update_data = dict()
        for key, value in data.items():
            if key in allow_change_list:
                update_data[key] = value
        return update_data

    @classmethod
    def reformatter_query(cls, data: dict):  # 格式化查询数据
        return data

    @classmethod
    def get_user(cls, query_dict: dict, unscoped: bool = False):  # 获取单个用户
        user = dao.User.get_user(query_dict=query_dict, unscoped=unscoped)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        return cls.formatter(user)

    @classmethod
    def query_users(cls, query_dict: dict, unscoped: bool = False):  # 获取用户列表
        (users, num) = dao.User.query_users(query_dict=query_dict,
                                            unscoped=unscoped)
        return [cls.formatter(user) for user in users], num

    @classmethod
    def insert_user(cls, data: dict = None):  # 插入用户
        if data is None:
            data = {}
        data = cls.reformatter_insert(data=data)
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            raise CustomError(500, 200, 'username or password must be given')
        user = dao.User.get_user(query_dict={'username': username},
                                 unscoped=False)
        if user is not None:
            raise CustomError(500, 200, 'username has be used')
        try:
            dao.User.insert_user(ctx=False, data=data)
        except Exception as e:
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_user(cls, username: str = '', data: dict = None):  # 更新用户
        if data is None:
            data = {}
        data = cls.reformatter_update(data)
        user = dao.User.get_user(query_dict={'username': username},
                                 unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        try:
            dao.User.update_user(ctx=False, username=username, data=data)
        except Exception as e:
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_user(cls, username: str = ''):  # 删除用户
        user = dao.User.get_user(query_dict={'username': username},
                                 unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        try:
            dao.User.delete_user(ctx=False, username=username)
        except Exception as e:
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True
