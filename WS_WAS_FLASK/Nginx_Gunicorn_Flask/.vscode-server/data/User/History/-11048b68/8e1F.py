from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import 
    @app.route('/')
    def hello_pybo():
        return 'Hello, Pybo!'

    return app