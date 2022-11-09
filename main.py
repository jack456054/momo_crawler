from flask import Flask, request
from flask_restful import Api, Resource

from utils.momo_crawler import crawler

app = Flask(__name__)
api = Api(app)


class ItemsList(Resource):
    def get(self):
        keyword = request.args.get('keyword')
        if not keyword:
            return {'message': 'keyword is required.'}, 400
        items, error_items = crawler(keyword, [], 1)
        if items:
            if error_items:
                return {'items': items, 'error_items': error_items}, 206
            else:
                return {'items': items, 'error_items': error_items}, 200
        else:
            return {'message': 'No items found.'}, 204


api.add_resource(ItemsList, '/items/')


if '__main__' == __name__:
    app.run(port=5000, debug=True)
