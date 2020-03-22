import datetime
import uuid

from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix
from google.cloud import datastore    
import mgrs
import yaml

from models import groups

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


api = Api(app, version='0.0.1', title='Social Support API',
    description='To retrieve Social Support groups',
)

groups_ns = api.namespace('groups', description='Social Support Groups')
@groups_ns.doc(
    params={
        'id': 'The identifyer of the group',
        'name': 'The name of the group',
        'lat': 'Latitude of the group location',
        'lng': 'Longitude of the group location',
    }
)

@groups_ns.route('/<id>')
class GroupById(Resource):
    def get(self, id = None):
        if id:
            group = groups.fetch_group('336202b985024ed88f6b201315d068cc')
            print(group)
            return (
                {
                    "hash" : group['hash'],
                    "name" : group['name'],
                    "description": group['description'],
                    "email": group['email']
                }
            )
    def put(self, id = None):
        return 'ok'



@groups_ns.route('/', methods = ['PUT', 'GET'])#, endpoint='group'
class Groups(Resource):
    def get(self):
        fetch_groups = groups.fetch_groups()
        response = list()
        for group in fetch_groups:
            response.append(
                {
                "hash" : group['hash'],
                "name" : group['name'],
                "description": group['description'],
                "email": group['email']
                }
            )
        return response

    @groups_ns.doc(
    params={
        'name': 'The name of the group',
        'description': 'A text with information about the group',
        'email': 'Main email contact of the organization',
        'lat': 'Latitude of the group location',
        'lng': 'Longitude of the group location',
    }
    )
    def put(self):
        name = request.form['name']
        description = request.form['description']
        email = request.form['email']
        lat = float(request.form['lat'])
        lng = float(request.form['lng'])      
        return 'ok'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
