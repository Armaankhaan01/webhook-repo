from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.webhook.routes import webhook
from app.api.routes import api
from app.extensions import init_extensions


# Creating our flask app
def create_app():

    app = Flask(__name__)
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/github_webhooks')
    app.config['GITHUB_WEBHOOK_SECRET'] = os.getenv('GITHUB_WEBHOOK_SECRET', '')
    CORS(app)

    init_extensions(app)
    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(api)
    @app.route('/')
    def index():
        return {'status': 'GitHub Webhook Receiver is running'}, 200
    
    return app
