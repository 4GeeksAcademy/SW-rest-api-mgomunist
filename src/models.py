from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in Favorite.query.filter_by(user_id=self.id).all()],
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    height = db.Column(db.String(50), default="unknown")
    mass = db.Column(db.String(50), default="unknown")
    hair_color = db.Column(db.String(50), default="unknown")
    skin_color = db.Column(db.String(50), default="unknown")
    eye_color = db.Column(db.String(50), default="unknown")
    birth_year = db.Column(db.String(50), default="unknown")
    gender = db.Column(db.String(50), default="unknown")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    diameter = db.Column(db.String(50), default="unknown")
    climate = db.Column(db.String(50), default="unknown")
    terrain = db.Column(db.String(50), default="unknown")
    population = db.Column(db.String(50), default="unknown")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    user = db.relationship('User', backref='favorites', lazy=True)
    planet = db.relationship('Planet', backref='favorites', lazy=True)
    people = db.relationship('People', backref='favorites', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "people": self.people.serialize() if self.people else None,
        }

