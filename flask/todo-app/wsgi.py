from app import create_app

application = create_app('production')

if __name__ == "__main__":
    application.run(host=application.config['HOST'], port=application.config['PORT'])