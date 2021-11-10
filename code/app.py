from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

# Crear el objeto de la interfaz web
app = Flask(__name__)

# Crear la variable de la key
app.secret_key = 'edu'

# Crear el objeto API
api = Api(app=app)

# Create the object that allow us to check credentials
jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)

items = []


class Item(Resource):
    # Parser here: that is the way of making that it belongs to the class, and not to any def. Now, it parser all the
    # REST methods
    # This object is going to parse the request
    parser = reqparse.RequestParser()
    # Parser is going to look in the JSON payload, but it also look in, for example, form payloads (HTML forms)
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field can not be blank!"
    )

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # return {"message": f"'{name}' item not found!"}, 404

        # Filtra items por la key 'name', quedandose solo con el primer (next) item que encuentre
        item = next(filter(lambda x: x['name'] == name, items), None)

        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        # Si el item <name> existe en la lista, devuelve un mensaje indicandolo
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'The item {name} is does exists.'}, 400

        data = Item.parser.parse_args()

        # data = request.get_json(silent=True)  # Silent=True hace que si hay un error, devuelva null
        item = {'name': name, 'price': data['price']}
        items.append(item)

        return item, 201

    def delete(self, name):
        global items  # You are saying that this 'items' is the 'items' declared out of this def (line 18)

        # Overwrite the 'items' with all the items that dont match the item we want to delete
        items = list(filter(lambda x: x['name'] != name, items))

        return {'message': 'Item deleted'}

    def put(self, name):  # Put updates an existing item. If it does not exist, it is created
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:  # If the item does not exist, we create it
            item = {'name': name, 'price': data['price']}
            items.append(item)

        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        if len(items) > 0:
            return {'items': items}, 200

        else:
            return {"message": f"items not found!"}, 404


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
