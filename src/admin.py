import os 
from flask_admin import Admin
from models import db, User, Planet, Favorite, People
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_admin import AdminIndexView

# Clase personalizada para el panel de administración
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True  

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

# Clase personalizada para ocultar 
class UserAdmin(ModelView):
    column_exclude_list = ['password']  # Oculta 
    form_excluded_columns = ['password']  

# Configurar el admin
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())

    # Agregar vistas de modelos
    admin.add_view(UserAdmin(User, db.session, category="Usuarios"))  
    admin.add_view(ModelView(Planet, db.session, category="Datos"))
    admin.add_view(ModelView(People, db.session, category="Datos"))
    admin.add_view(ModelView(Favorite, db.session, category="Relaciones"))

