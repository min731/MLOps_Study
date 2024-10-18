import os
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from .utils.logger import setup_logger
from .config import config

# 데이터베이스 인스턴스 생성
db = SQLAlchemy()

def create_app(config_name=None):
    """애플리케이션 팩토리 함수"""
    app = Flask(__name__)

    # 환경 변수에서 설정 가져오기 (기본값은 'development')
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    
    # 설정 로드
    app.config.from_object(config[config_name])
    
    # 데이터베이스 초기화
    db.init_app(app)

    # API 초기화
    api = Api(app, version='1.0', title='Task API', description='A simple Task API')

    # 로거 설정
    setup_logger(app)

    # 뷰 등록
    from .views.task_view import api as task_ns
    api.add_namespace(task_ns)

    # 데이터베이스 생성
    with app.app_context():
        db.create_all()

    return app