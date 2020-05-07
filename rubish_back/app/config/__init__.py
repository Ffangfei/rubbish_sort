#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:53 PM
# @Author  : suchang
# @File    : __init__.py.py

import os
from datetime import timedelta


class Config:  # 从数据库获取配置信息
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    PATIENTS_PRE_PAGE = 20
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    THREADED = True
    SQLALCHEMY_DATABASE_URI = \
        "mysql+pymysql://root:wshwoaini@localhost:3306/rubbish?charset=utf8mb4"

    CAPTCHA_EXPIRE = 300

    JWT_AUTH_URL_RULE = '/login'
    JWT_ALGORITHM = 'HS256'
    JWT_LEEWAY = timedelta(seconds=300)
    JWT_VERIFY_CLAIMS = ['signature', 'exp', 'nbf', 'iat']
    JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)
    JWT_EXPIRATION_DELTA = timedelta(seconds=7200)
    JWT_REQUIRED_CLAIMS = ['exp', 'iat', 'nbf']
    JWT_AUTH_HEADER_PREFIX = 'bearer'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
