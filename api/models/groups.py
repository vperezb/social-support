import datetime
import uuid

from google.cloud import datastore    
import mgrs
import yaml

with open("credentials.yaml", 'r') as stream:
    try:
       __credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Init datastore and api

datastore_client = datastore.Client(__credentials['project_id'])

# Functions

def store_group(name, description, url, lat, lng, email):
    translated_mgrs = mgrs.MGRS().toMGRS(lat, lng).decode('UTF-8')
    entity = datastore.Entity(key=datastore_client.key('group'))
    public_info_to_put = {
        'timestamp': datetime.datetime.now(),
        'lat': lat,
        'lng': lng,
        'email': email,
        'mgrs': translated_mgrs,
        'mgrs_6': translated_mgrs[:6],
        'mgrs_8': translated_mgrs[:8],
        'name': name,
        'description': description,
        'status' : 'disabled',
        'hash': uuid.uuid4().hex,
    }

    private_info_to_put = public_info_to_put.copy()

    private_info_to_put['p_hash'] = uuid.uuid4().hex
    entity.update(private_info_to_put)
    print(datastore_client.put(entity))
    return public_info_to_put
    


def fetch_group(hash):
    query = datastore_client.query(kind='group')
    query.add_filter('hash', '=', hash)
    groups = query.fetch(limit=1)
    for group in groups:
        return group


def fetch_groups():#lat, lng
    #needs_mgrs = mgrs.MGRS().toMGRS(lat, lng).decode('UTF-8')
    query = datastore_client.query(kind='group')
    #query.add_filter('status', '=',  'toconfirm')
    #query.add_filter('status', '=',  'enabled')
    #query.add_filter('mgrs_6', '=', needs_mgrs[:6])
    groups = query.fetch(limit=20)
    return groups