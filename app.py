from flask import Flask
from flask_cors import CORS
from config import config
from routes import routes

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_app()
        self.register_routes()

    def configure_app(self):
        self.app.config.from_object(config)
        CORS(self.app)

    def register_routes(self):
        # Register the /v1 API blueprint
        self.app.register_blueprint(routes, url_prefix='/api')

    def start(self):
        self.app.run(host='0.0.0.0', port=config.PORT)

if __name__ == '__main__':
    app_instance = App()
    app_instance.start()