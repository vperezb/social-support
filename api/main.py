import datetime
import uuid
#import pdb; pdb.set_trace()

from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
#from werkzeug.contrib.fixers import ProxyFix
from google.cloud import datastore    
import mgrs
import yaml

from models import groups

app = Flask(__name__)
CORS(app)
#app.wsgi_app = ProxyFix(app.wsgi_app)


api = Api(app, version='0.0.1', title='Social Support API',
    description='To retrieve Social Support groups',
)

group_fields = api.model('Group', {
    'name': fields.String(description='The name of the group', required=True),
    'description': fields.String(description='This method should be used everytime we want to create a new group', required=True),
    'url': fields.String(description='The main webpage of the organization/group', required=True),
    'email': fields.String(description='Main email contact of the organization'),
    #'type': fields.String(description='The object type', enum=['A', 'B']),
    'lat': fields.Float(),
    'lng': fields.Float(),
    })

groups_ns = api.namespace('groups', description='Social Support Groups')

@groups_ns.route('/<id>')
class GroupById(Resource):
    @groups_ns.doc(params={'id': 'The identifyer of the group',})
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
    # def put(self, id = None):
    #     return 'ok'



@groups_ns.route('/', methods = ['POST', 'GET'])#, endpoint='group'
class Groups(Resource):
    @groups_ns.doc(
        description = 'This method can be used to retrieve all groups',
        # params={
        #     'lat': 'Latitude of the group location',
        #     'lng': 'Longitude of the group location',
        # }
    )
    def get(self):
        fetch_groups = groups.fetch_groups()
        items = list()
        for group in fetch_groups:
            items.append(
                {
                "hash" : group['hash'],
                "name" : group['name'],
                "description": group['description'],
                "email": group['email']
                }
            )
        return {'items' : items}

    @groups_ns.doc(
        description = 'This method should be used everytime we want to create a new group',
        model = 'Group',
        body = group_fields
    )
    
    #@groups_ns.apiexpect(group.modesl)
    def post(self):
        json_data = request.get_json(force=True)
        name = json_data['name']
        description = json_data['description']
        url = json_data['url']
        email = json_data['email']
        lat = float(json_data['lat'])
        lng = float(json_data['lng'])
        info_stored = groups.store_group(name, description, url, lat, lng, email)
        info_stored['timestamp'] = info_stored['timestamp'].strftime("%m/%d/%Y, %H:%M:%S")
        return {'info_stored': info_stored}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
