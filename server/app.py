#!/usr/bin/env python3

from flask import Flask, request   # <-- add request here
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Plant


app = Flask(__name__)

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)   # ✅ enable flask db commands

api = Api(app)

# --- resources ---
class Plants(Resource):
    def get(self):
        plants = [p.to_dict() for p in Plant.query.all()]
        return plants, 200

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 201


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404


# register resources
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
