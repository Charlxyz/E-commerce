# Config Flask
from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder='./templates', static_folder='./static')

# Config API
api = Api(app)

# Config sécurité
bcrypt = Bcrypt(app)

# Config secret key
app.config['SECRET_KEY'] = 'secret_key'