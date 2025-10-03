"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, FavoritoPlaneta, FavoritoPersonaje
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# **** Users *****

@app.route('/users', methods=['GET'])
def get_todos_users():

    users = User.query.all()
    users = list(map(lambda u: u.serialize(), users))
    return jsonify(users), 200

@app.route('/user/favoritos', methods=['GET'])
def get_user_favoritos():

    user = User.query.first()
    favoritos = Favorito.query.filter_by(user_id = user.id).all()
    favoritos =  list(map(lambda f: f.serialize(), favoritos))
    return jsonify(favoritos), 200

# **** Personajes *****

@app.route('/personajes', methods=['GET'])
def get_todos_personajes():

    personajes = Personaje.query.all()
    personajes = list(map(lambda p: p.serialize(), personajes))
    return jsonify(personajes), 200

@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):

    personaje = Personaje.query.get(personaje_id)
    return jsonify(personaje.serialize()), 200

# **** Planetas *****

@app.route('/planetas', methods=['GET'])
def get_todos_planetas():

    planetas = Planeta.query.all()
    planetas = list(map(lambda p: p.serialize(), planetas))
    return jsonify(planetas), 200

@app.route('/planeta/<int:planet_id>', methods=['GET'])
def get_planeta(planeta_id):

    planeta = Planeta.query.get(planeta_id)
    return jsonify(planeta.serialize()), 200



# **** Favoritos de Personajes ****

@app.route('/favoritos/personajes', methods=['GET'])
def get_favoritos_personajes():
    favoritos = FavoritoPersonaje.query.all()
    favoritos = list(map(lambda f: f.serialize(), favoritos))
    return jsonify(favoritos), 200

@app.route('/favoritos/personaje/<int:personaje_id>', methods=['POST'])
def add_favorito_personaje(personaje_id):

    user = User.query.first()
    favorito = FavoritoPersonaje.query.filter_by(user_id=user.id, personaje_id=personaje_id).first()
    if favorito:
        return jsonify({"mensaje": "Ya existe en favoritos"}), 400
    nuevo_fav = FavoritoPersonaje(user_id=user.id, personaje_id=personaje_id)
    db.session.add(nuevo_fav)
    db.session.commit()
    return jsonify(favorito.serialize()), 201

@app.route('/favoritos/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_favorito_personaje(personaje_id):

    user = User.query.first()
    favorito = FavoritoPersonaje(user_id=user.id, personaje_id=personaje_id)
    if not favorito:
        return jsonify({"mensaje": "No existe este favorito"}), 404
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"mensaje": "Personaje Favorito Eliminado"}), 200

# **** Favoritos de Planetas ****

@app.route('/favoritos/planetas', methods=['GET'])
def get_favoritos_planetas():
    favoritos = FavoritoPlaneta.query.all()
    favoritos = list(map(lambda f: f.serialize(), favoritos))
    return jsonify(favoritos), 200

@app.route('/favoritos/planeta/<int:planeta_id>', methods=['POST'])
def add_favorito_planeta(planeta_id):

    user = User.query.first()
    favorito = FavoritoPlaneta.query.filter_by(user_id=user.id, planeta_id=planeta_id).first()
    if favorito:
        return jsonify({"mensaje": "Ya existe en favoritos"}), 400
    nuevo_fav = FavoritoPlaneta(user_id=user.id, planeta_id=planeta_id)
    db.session.add(nuevo_fav)
    db.session.commit()
    return jsonify(nuevo_fav.serialize()), 201

@app.route('/favoritos/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_favorito_planeta(planeta_id):

    user = User.query.first()
    favorito = FavoritoPlaneta(user_id=user.id, planeta_id=planeta_id)
    if not favorito:
        return jsonify({"mensaje": "No existe este favorito"}), 404
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"mensaje": "Planeta Favorito Eliminado"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
