import os
from flask_admin import Admin
from models import db, User, Planet, Favorite, People  # Asegúrate de importar todos los modelos necesarios
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'  # Tema de Bootstrap para la interfaz
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session))      # Modelo User
    admin.add_view(ModelView(Planet, db.session))    # Modelo Planet
    admin.add_view(ModelView(Favorite, db.session))  # Modelo Favorite
    admin.add_view(ModelView(People, db.session))    # Modelo People

    # Puedes duplicar la línea para agregar más modelos si es necesario
    # admin.add_view(ModelView(YourModelName, db.session))
