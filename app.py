import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Dessert, Order, db_drop_and_create_all
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    db_drop_and_create_all()
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # no authorization
    @app.route('/')
    def check_connection():
        return "Hello, Welcome to Evie's cafe, Enjoy dessert!"

    # no authorization
    @app.route('/desserts')
    def get_all_desserts():
        dessert_list = Dessert.query.order_by(Dessert.id).all()
        desserts = [dessert.format() for dessert in dessert_list]

        return jsonify({
            "success": True,
            "desserts": desserts
        }), 200

    # manager
    @app.route('/desserts', methods=['POST'])
    @requires_auth('post: desserts')
    def post_dessert(token):

        received_data = request.get_json()
        dessert_name = received_data.get('name', None)
        dessert_price = received_data.get('price', None)

        if (dessert_name is None) or (dessert_price is None):
            abort(422)

        try:
            new_dessert = Dessert(name=dessert_name, price=dessert_price)
            new_dessert.insert()
            return jsonify({
                'success': True,
                'created_dessert': new_dessert.format()})

        except:
            abort(422)

    # manager

    @app.route('/desserts/<int:dessert_id>', methods=['PATCH'])
    @requires_auth('patch: desserts')
    def patch_dessert(token, dessert_id):
        dessert = Dessert.query.get(dessert_id)
        if dessert is None:
            abort(404)

        try:
            received_data = request.get_json()
            new_name = received_data.get('name', None)
            new_price = received_data.get('price', None)

            if (new_name is None) and (new_price is None):
                abort(422)
            if new_name:
                dessert.name = new_name

            if new_price:
                dessert.price = new_price

            dessert.update()

        except:
            abort(422)

        return jsonify({
            'success': True,
            'updated_dessert': dessert.format()
        })

    # manager
    @app.route('/desserts/<int:id>', methods=['DELETE'])
    @requires_auth('delete: desserts')
    def delete_dessert(token, id):
        dessert = Dessert.query.get(id)
        if not dessert:
            abort(404)
        try:
            dessert.delete()
            return jsonify({
                'success': True,
                'deleted': dessert.id
            }), 200
        except Exception:
            abort(500)

   #manager and customer
    @app.route('/orders/<int:id>', methods=['GET'])
    @requires_auth('get:orders')
    def get_orders_by_id(token, id):
        try:
            order_ = Order.query.get(id)
            return jsonify({
                'success': True,
                'order': order_.format()
            }), 200
        except:
            abort(404)
   #customer and manager

    @app.route('/orders', methods=['POST'])
    @requires_auth('"post: orders"')
    def post_orders(token):
        received_data = request.get_json()
        new_customer = received_data.get('customer', None)
        new_items = received_data.get('items', None)
        desserts_items = Dessert.query.filter(
            Dessert.name.in_(new_items)).all()

        if (new_customer is None) or (new_items is None):
            abort(422)

        try:
            new_order = Order(customer=new_customer)
            new_order.items = desserts_items
            new_order.insert()

            return jsonify({
                'success': True,
                'new_order': new_order.format()
            })

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
