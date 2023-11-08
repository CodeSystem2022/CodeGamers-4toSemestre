from flask import Flask
from config import Config
from app.models import  db, Users
from flask_login import LoginManager

app = Flask(__name__)
#app.config.from_object(Config)
app.config['SECRET_KEY'] = 'pYajmB^75UXA6#h^$$2Jsq@K&$zumsm$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frikio.db'
app.config['DEBUG'] = True
db.init_app(app)  # inicializamos la aplicacion con la extension

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # La vista de inicio de sesión

# Implementa la lógica para cargar un usuario por su ID
@login_manager.user_loader
def load_user(id):
   return Users.query.get(int(id))

from app import routes
