from app.handler import auth_blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, jsonify, Blueprint
import app.controller as controller
import app.services as service
from flask_jwt import jwt_required, current_identity
from app.utils import CustomError


@auth_blueprint.route('/tokens', methods=['GET'])
@jwt_required()
def refresh_token():  # 刷新token
    if current_identity is not None:
        try:
            token = controller.new_token(current_identity)
        except Exception as e:
            return jsonify(code=403, msg="请先登录"), 200
        return jsonify({"token": token.decode('utf-8'), "msg": ""}), 200
    return jsonify(code=403, msg="请先登录"), 200


@auth_blueprint.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():  # 获取当前登陆用户
    if current_identity is not None:
        user = dict(current_identity)
        return jsonify({'current_user': user, 'msg': ''}), 200
    return jsonify(code=403, msg="请先登录"), 200


@auth_blueprint.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():  # 更改当前用户密码
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    uuid = request.json.get('uuid', None)
    code = request.json.get('code', None)
    try:
        controller.change_password(username, password, uuid, code)
    except CustomError as e:
        return jsonify(code=e.code, msg=e.err_info), e.status_code
    return jsonify(code=200, msg="success"), 200


@auth_blueprint.route("/401", methods=["GET"])
def error_401():  # 401返回错误
    return jsonify({
        'code': 401,
        'msg': '',
    }), 401


@auth_blueprint.route('/captcha', methods=['GET'])
def get_captcha():  # 获取验证码
    try:
        (id, path) = controller.CaptchaController.new_captcha()
    except Exception as e:
        return jsonify(code=500, msg=str(e)), 500
    return jsonify(code=200, uuid=id, path=path)
