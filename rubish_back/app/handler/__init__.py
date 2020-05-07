from flask import Blueprint

auth_blueprint = Blueprint('auth_blueprint', __name__)
user_blueprint = Blueprint('user_blueprint', __name__)

from . import auth
