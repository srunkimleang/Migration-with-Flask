from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onetoone.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return 'Hello World!!!'


## Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    from_shop = db.relationship('Shop', backref='product', lazy=True)

    def __init__(self, name, description):
        self.name=name
        self.description=description
class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    location = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    def __init__(self, name, location):
        self.name=name
        self.location=location

## Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')
## Shop Schema
class ShopSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location')

## Init schema
product_schema = ProductSchema()
shop_schema = ShopSchema()
products_schema = ProductSchema(many=True)
shops_schema = ShopSchema(many=True)

#create  A Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    new_prodcut = Product(name, description)
    db.session.add(new_prodcut)
    db.session.commit()
    return product_schema.jsonify(new_prodcut)
#create  A Shop
@app.route('/shop', methods=['POST'])
def add_shop():
    name = request.json['name']
    location = request.json['location']
    new_shop = Shop(name, location)
    db.session.add(new_shop)
    db.session.commit()
    return shop_schema.jsonify(new_shop)

# Get all the Shop
@app.route('/shop', methods=['GET'])
def get_shop():
    all_shops = Shop.query.all()
    result = shops_schema.dump(all_shops)
    return jsonify(result)
# Get all the Product
@app.route('/product', methods=['GET'])
def get_product():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

## Get Single Product
@app.route('/product/<id>', methods=['GET'])
def single_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

## Update Specific Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']

    product.name = name
    product.description = description

    db.session.commit()
    return product_schema.jsonify(product)

## Delete Single Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

##Run server
if __name__ == '__main__':
    app.run(debug=True)