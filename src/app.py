import os
from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flasgger import Swagger
from flask_migrate import Migrate
from flask_cors import CORS
from admin import setup_admin
from utils import APIException, generate_sitemap
import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SECRET_KEY'] = 'your-secret-key'

# Inicializar extensiones
db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)
migrate = Migrate(app, db)
CORS(app)
setup_admin(app)  # Configuración del admin

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_type = db.Column(db.String(50), nullable=False)  # 'planet' o 'character'
    item_id = db.Column(db.Integer, nullable=False)

# Manejo de errores personalizado con APIException
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generación dinámica de sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Rutas

# Ruta de login para obtener el token JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or user.password != password:
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
    return jsonify({'token': access_token}), 200

# CRUD de personajes
@app.route('/characters', methods=['POST'])
@jwt_required()
def add_character():
    data = request.get_json()
    if 'name' not in data or 'species' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    new_character = Character(name=data['name'], species=data['species'])
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"message": "Character added successfully"}), 201

@app.route('/characters/<int:id>', methods=['GET'])
@jwt_required()
def get_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    return jsonify({'id': character.id, 'name': character.name, 'species': character.species}), 200

# CRUD de favoritos
@app.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    data = request.get_json()
    favorite = Favorite(user_id=data['user_id'], favorite_type=data['favorite_type'], item_id=data['item_id'])
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite added successfully"}), 201

@app.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    current_user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    return jsonify([{'favorite_type': f.favorite_type, 'item_id': f.item_id} for f in favorites]), 200

# Manejo de errores 404
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(debug=True)