# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route('/pets/<int:id>')
def get_pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        body = pet.to_dict()
        status = 200
    else:
        body = {'error': f'Pet {id} not found'}
        status = 404

    return make_response(body, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter(Pet.species == species).all()

    if pets:
        pets_list = [pet.to_dict() for pet in pets]
        body = {'count': len(pets_list), 'pets': pets_list}
        status = 200
    else:
        body = {'error': f'Species {species} does not exist'}
        status = 404
    
    return make_response(body, status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
