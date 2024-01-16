#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


@app.route('/')
def home():
    return {'Hello': 'Welcome to my api'}


class HeroListResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        heroes_list = [
            {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name}
            for hero in heroes
        ]
        return jsonify(heroes_list)


api.add_resource(HeroListResource, '/heroes')


class HeroResource(Resource):
    def get(self, hero_id):
        hero = Hero.query.get_or_404(hero_id)
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [
                {
                    'id': hero_power.power.id,
                    'name': hero_power.power.name,
                    'description': hero_power.power.description
                }
                for hero_power in hero.hero_powers
            ]
        }
        return jsonify(hero_data)


api.add_resource(HeroResource, '/heroes/<int:hero_id>')


class PowerListResource(Resource):
    def get(self):
        powers = Power.query.all()
        powers_list = [
            {'id': power.id, 'name': power.name, 'description': power.description}
            for power in powers
        ]
        return jsonify(powers_list)


api.add_resource(PowerListResource, '/powers')


class PowerResource(Resource):
    def get(self, power_id):
        power = Power.query.get_or_404(power_id)
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)


api.add_resource(PowerResource, '/powers/<int:power_id>')


class PowerUpdateResource(Resource):
    def patch(self, power_id):
        power = Power.query.get_or_404(power_id)
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        else:
            return jsonify({'error': 'Missing description field'}), 400


api.add_resource(PowerUpdateResource, '/powers/<int:power_id>')


class HeroPowerResource(Resource):
    def post(self):
        data = request.get_json()
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')
        strength = data.get('strength')

        if not power_id or not hero_id or not strength:
            return jsonify({'error': 'Missing required fields'}), 400

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            return jsonify({'error': 'Hero or Power not found'}), 404

        hero_power = HeroPower(hero=hero, power=power, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [
                {
                    'id': hero_power.power.id,
                    'name': hero_power.power.name,
                    'description': hero_power.power.description
                }
                for hero_power in hero.hero_powers
            ]
        }
        return jsonify(hero_data), 201


api.add_resource(HeroPowerResource, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555)
