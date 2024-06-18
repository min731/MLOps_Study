from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import check_view
    app.register_blueprint(check.bp)

    return app