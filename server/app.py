

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200, {'Content-Type': 'application/json'})

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return make_response(jsonify({}), 404, {'Content-Type': 'application/json'})

    if request.method == 'GET':
        return make_response(jsonify(bakery.to_dict()), 200, {'Content-Type': 'application/json'})
    
    elif request.method == 'PATCH':
        data = request.form
        for attr, value in data.items():
            setattr(bakery, attr, value)
        
        db.session.commit()

        bakery_dict = bakery.to_dict()

        return make_response(jsonify(bakery_dict), 200, {'Content-Type': 'application/json'})

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    baked_good = BakedGood(name=data['name'], price=data['price'], bakery_id=data['bakery_id'])
    db.session.add(baked_good)
    db.session.commit()
    return make_response(jsonify(baked_good.to_dict()), 201, {'Content-Type': 'application/json'})

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(jsonify(baked_goods_by_price_serialized), 200, {'Content-Type': 'application/json'})

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        return make_response(jsonify({}), 404, {'Content-Type': 'application/json'})

    db.session.delete(baked_good)
    db.session.commit()
    return make_response(jsonify({}), 200, {'Content-Type': 'application/json'})

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()

    if not most_expensive:
        return make_response(jsonify({}), 404, {'Content-Type': 'application/json'})

    most_expensive_serialized = most_expensive.to_dict()
    return make_response(jsonify(most_expensive_serialized), 200, {'Content-Type': 'application/json'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
