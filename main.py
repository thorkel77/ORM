from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy


import passlib.hash import sha256_crypt

from models import *

import config

app = Flask(__name__)
app.config.from_object(config.DeveloppementConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = "http://localhost/phpmyadmin/db_import.php?db=api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db= SQLAlchemy(app)

app.config['SQLALCHEMYECHO']= True

with app.app_context():
    db.init_app(app)
class brands (db.model):
    __tablename__ = 'brands'

    brand_id = db.Column(db.Integer, primary_key=True )
    brand_name = db.Column(db.String(30) )

    product = db.relationship('products', backref='brand')

    def __repr__(self):
        return '<brands {}>'.format(self.brand_name)

class categories(db.modelodels):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(30))

    category = db.relationship('products', backref='category')
    def __repr__(self):
        return '<categories {}>'.format(self.category_name)

class customers(db.model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.column(db.String(255))
    last_name = db.column(db.string(255))
    phone = db.column(db.integer)
    email = db.column(db.string(50))
    street = db.column(db.string(50))
    city = db.column(db.string(255))
    zip_code = db.column(db.string(50))


class orders (db.model):
    __tablename__ = 'orders'

    order_id = db.column(db.integer, primary_Key= True)
    customers_id = db.Column('customer_id', db.integer, db.ForeignKey('customers.customer_id'))
    order_status = db.column(db.string(50))
    required_date = db.column(db.string(50))
    shipped_date = db.column(db.string(50))
    store_id = db.Column('store_id', db.integer, db.ForeignKey('stores.store_id'))
    staff_id = db.Column('staff_id', db.integer, db.ForeignKey('staffs.staff_id'))


class order_items(db.model):
    __tablename__ = 'order_items'

    order_id = db.Column('order_id', db.integer, db.ForeignKey('orders.order_id'))
    item_id = db.column(db.integer, primary_Key= True)
    product_id = db.Column('product_id', db.integer, db.ForeignKey('products.product_id'))
    quantity  = db.colum(db.integer)
    list_price = db.column(db.string(50))
    discount = db.column(db.string(50))

 class Products(db.model):
    __tablename__ = 'products'

    product_id = db.column(db.integer, primary_Key= True)
    product_name = db.column(db.string(30))
    brand_id = db.Column('brand_id', db.integer, db.ForeignKey('brands.brand_id'))
    category_id = db.Column('category_id', db.integer, db.ForeignKey('categories.category_id'))
    model_year = db.column(db.string(30))
    list_price = db.column(db.string(30))


class staffs(db.model):
    __tablename__ = 'staffs'

    staff_id = db.column(db.integer, primary_Key= True)
    first_name = db.column(db.string(255))
    last_name = db.column(db.string(255))
    email = db.column(db.string(20))
    phone = db.column(db.integer)
    active = db.column(db.string(30))
    store_id = db.Column('store_id', db.integer, db.ForeignKey('stores.store_id'))
    manager_id = db.column(db.integer)



stock = db.Table('stocks',
        db.Column('store_id', db.integer, db.ForeignKey('stores.store_id'), primary_key=True),
        db.Column('product_id', db.integer, db.ForeignKey('products.products_id'), primary_key=True),
        db.Column('quantity', db.Integer)

)


class Stores(db.Model):
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer, primary_key=True )
    store_name = db.Column(db.String(255))
    phone = db.Column(db.string(10))
    email = db.Column(db.string(255))
    street = db.Column(db.string(255))
    City = db.Column(db.string(255))
    state = db.Column(db.string(255))
    zip_code = db.Column(db.Integer)

    category_stocks = db.relationship('Products', secondary= stock, backref= db.backref('contains', lazy= 'dynamic'))

    category_staffs= db.relationshiip('staffs',  backref='staff')

    category_orders = db.relationship('Orders', backref= 'store')

    def __repr__(self):
        return '<stores {}>'.format(self.store_name)


store = Stores(store_name= "Adidas", phone="0652481988", email="denys.2launay@gmail.com", street="12 rue anatole france", city= "Paris", state= "France", zip_code= "1234" )
db.session.add(store)


product= Products(product_name="produit", brand=brand, category=category, model_year= '2020-05-15 01:12:25', list_price=30 )
db.session.add(product)

product.contains.append(store, quantity=1)

customer= customers(first_name="blalkd", last_name = "jfjd", phone="0645781592", email= "denu@ejfdf.com", street="12 rue anatole france", city= "Paris",zip_code= "1234"  )
db.session.add(customer)

staff = staffs(first_name="blalkd", last_name = "jfjd", phone="0645781592", email= "denu@ejfdf.com", active=True, staff=store, manager_id=1)
db.session.add(staff)

order = orders(customer=customer, order_status=1, order_date='2020-05_15 01:12:25', required_date='2020-05_15 01:12:25', shipped_date= '2020-05_15 01:12:25')
db.session.add(order)

order_item = order_items(order=order, product=product, quantity=22, list_price=10, discount=5)
db.session.add(order_item)





if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)







