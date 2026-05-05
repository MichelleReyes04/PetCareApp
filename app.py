from flask import Flask, session
from routes.menu_routes import menu_bp
from routes.auth_routes import auth_bp
from utils import oauth
from dotenv import load_dotenv
import openai
import os

#load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

oauth.init_app(app)


# Google Oauth Config
# Get client_id and client_secret from environment variables
# For developement purpose you can directly put it 
# here inside double quotes

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.context_processor
def inject_user():
    return dict(user=session.get('user'))

app.register_blueprint(menu_bp)
app.register_blueprint(auth_bp)



if __name__ == '__main__':
    app.run(debug=True)