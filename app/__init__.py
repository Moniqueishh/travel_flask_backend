from flask import Flask

from config import Config

from .api.routes import api


from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager

from flask_cors import CORS


app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})

login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login.init_app(app)
# set up a re-route for unauthorized access
login.login_view = 'auth.loginPage'

app.register_blueprint(api)



from . import routes

