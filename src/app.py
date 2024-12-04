import os
from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flasgger import Swagger
from flask_migrate import Migrate
from flask_cors import CORS
from admin import setup_admin
from utils import APIException, generate_sitemap
from models import db, User, People, Planet, Favorite  # Importar modelos
import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)
swagger = Swagger(app)
migrate = Migrate(app, db)
CORS(app)
setup_admin(app)

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# [GET] /people: Listar todos los personajes
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

# [GET] /people/<int:people_id>: Obtener un personaje por ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"message": "Person not found"}), 404
    return jsonify(person.serialize()), 200

# [GET] /planets: Listar todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

# [GET] /planets/<int:planet_id>: Obtener un planeta por ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# [GET] /users: Listar todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# [GET] /users/favorites: Listar favoritos del usuario actual
@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites():
    current_user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    return jsonify([fav.serialize() for fav in favorites]), 200

# [POST] /favorite/planet/<int:planet_id>: Añadir un planeta favorito
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
@jwt_required()
def add_favorite_planet(planet_id):
    current_user_id = get_jwt_identity()
    new_favorite = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet added successfully"}), 201

# [POST] /favorite/people/<int:people_id>: Añadir un personaje favorito
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
@jwt_required()
def add_favorite_people(people_id):
    current_user_id = get_jwt_identity()
    new_favorite = Favorite(user_id=current_user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Favorite character added successfully"}), 201

# [DELETE] /favorite/planet/<int:planet_id>: Eliminar un planeta favorito
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_planet(planet_id):
    current_user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"message": "Favorite planet not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet deleted successfully"}), 200

# [DELETE] /favorite/people/<int:people_id>: Eliminar un personaje favorito
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_people(people_id):
    current_user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(user_id=current_user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"message": "Favorite character not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite character deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)