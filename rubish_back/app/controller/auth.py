from flask_jwt import JWT, JWTError, logger
from werkzeug.security import safe_str_cmp, check_password_hash
import app.dao as dao
from werkzeug.local import LocalProxy
from sqlalchemy.exc import OperationalError, IntegrityError, DataError
from flask import request, current_app, jsonify, _request_ctx_stack
from datetime import datetime
from collections import OrderedDict
import os
import jwt
from app.utils.error import CustomError
from app.controller.user import UserController


def jwt_init():  # 初始化jwt组件
    custom_jwt = JWT()

    @custom_jwt.authentication_handler
    def authenticate(username, password):
        try:
            user = dao.User.get_user(query_dict={"username": username})
        except (OperationalError, IntegrityError, DataError) as e:
            raise JWTError('Bad Request', str(e))
        if user and check_password_hash(user['password_hash'], password):
            return user
        else:
            return None

    @custom_jwt.jwt_payload_handler
    def jwt_payload(identity):
        return new_payload(identity)

    @custom_jwt.identity_handler
    def identity(payload):
        user_id = payload['identity'].get("id")
        user = dao.User.get_user(query_dict={"id": user_id})
        return user

    @custom_jwt.auth_response_handler
    def auth_response(access_token, identity):
        return jsonify({'code': 200, 'token': access_token.decode('utf-8')})

    @custom_jwt.jwt_error_handler
    def jwt_error(error):
        logger.error(error)
        return jsonify(OrderedDict([('code', 401), ('msg', error.description)
                                    ])), 200, error.headers

    @custom_jwt.auth_request_handler
    def auth_request():
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        criterion = [username, password]

        if not all(criterion):
            raise JWTError('Bad Request', '登录选项错误')


        _jwt = LocalProxy(lambda: current_app.extensions['jwt'])

        identity_data = _jwt.authentication_callback(username, password)

        if identity_data:
            access_token = _jwt.jwt_encode_callback(identity_data)
            return _jwt.auth_response_callback(access_token, identity_data)
        else:
            raise JWTError('Bad Request', '用户或密码错误')

    return custom_jwt


def new_payload(identity):  # 生成新的payload
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': dict(identity)}


def new_token(identity):  # 生成新的token
    secret = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

    payload = new_payload(identity)
    missing_claims = list(set(required_claims) - set(payload.keys()))

    if missing_claims:
        raise RuntimeError('Payload is missing required claims: %s' %
                           ', '.join(missing_claims))

    headers = None

    return jwt.encode(payload, secret, algorithm=algorithm, headers=headers)


def change_password(username: str = None,
                    password: str = None):  # 更改用户密码

    if username or password is None:
        raise CustomError(500, 200, "请给与username和password")
    users, total = UserController.query_users(
        query_dict={'username': username})
    if total == 0:
        raise CustomError(500, 200, "用户不存在")
    UserController.update_user(username=username, data={'password': password})
