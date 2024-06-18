from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import check
    app.register_blueprint(check.bp)

    return app