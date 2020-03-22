import datetime
import uuid

from flask import Flask, render_template, request, jsonify
from google.cloud import datastore    
import mgrs
import yaml

with open("credentials.yaml", 'r') as stream:
    try:
       __credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

datastore_client = datastore.Client(__credentials['project_id'])

app = Flask(__name__)

def store_need(email, lat, lng, title, description, type):
    need_mgrs = mgrs.MGRS().toMGRS(lat, lng).decode('UTF-8')
    entity = datastore.Entity(key=datastore_client.key('User', email, 'need'))
    entity.update({
        'timestamp': datetime.datetime.now(),
        'lat': lat,
        'lng': lng,
        'mgrs': need_mgrs,
        'mgrs_6': need_mgrs[:6],
        'mgrs_8': need_mgrs[:8],
        'title': title,
        'description': description,
        'type': type,
        'status' : 'enabled',
        'hash': uuid.uuid4().hex,
        'p_hash': uuid.uuid4().hex
    })

    datastore_client.put(entity)


def store_group(name, description, url, lat, lng, email):
    translated_mgrs = mgrs.MGRS().toMGRS(lat, lng).decode('UTF-8')
    entity = datastore.Entity(key=datastore_client.key('group'))
    entity.update({
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
        'p_hash': uuid.uuid4().hex
    })

    datastore_client.put(entity)


def store_enroll(email, phone, comment, need_hash):
    entity = datastore.Entity(key=datastore_client.key('User', email, 'enroll'))
    entity.update({
        'timestamp': datetime.datetime.now(),
        'status' : 'just_enrolled',
        'email': email,
        'phone': phone,
        'comment': comment,
        'need_hash': need_hash
    })

    datastore_client.put(entity)


def change_need_status(key, status):
    task = datastore_client.get(key)
    task['status'] = status
    datastore_client.put(task)
    return True


def fetch_need(hash):
    query = datastore_client.query(kind='need')
    query.add_filter('hash', '=', hash)
    needs = query.fetch(limit=1)
    for need in needs:
        return need


def fetch_group(hash):
    query = datastore_client.query(kind='group')
    query.add_filter('hash', '=', hash)
    groups = query.fetch(limit=1)
    for group in groups:
        return group

def fetch_groups(lat, lng):
    needs_mgrs = mgrs.MGRS().toMGRS(lat, lng).decode('UTF-8')
    query = datastore_client.query(kind='group')
    #query.add_filter('status', '=',  'toconfirm')
    #query.add_filter('status', '=',  'enabled')
    #query.add_filter('mgrs_6', '=', needs_mgrs[:6])
    groups = query.fetch(limit=20)
    return groups

def fetch_needs(lat, lng):
    needs_mgrs = mgrs.MGRS().toMGRS(lat, lng).decode('UTF-8')
    query = datastore_client.query(kind='need')
    #query.add_filter('status', '=',  'toconfirm')
    query.add_filter('status', '=',  'enabled')
    query.add_filter('mgrs_6', '=', needs_mgrs[:6])
    needs = query.fetch(limit=20)
    return needs


@app.route('/')
def root():
    groups = fetch_groups(1,1)
    return render_template(
        'groups.html',
        groups =groups)


@app.route('/groups')
def groups():
    return render_template(
        'groups.html')

@app.route('/jotason')
def summary():
    d = {
        'test':'hola marico',
        'enough':'?'
    }
    return jsonify(d)

@app.route('/offer', methods=['GET'])
def offer():
    z = request.args.get('z')
    if z:
        lat, lng, zoom, distance = z.split(',')

        return render_template(
            'offer.html', 
            context={'key':__credentials['api_key']}, 
            zone={'lat':lat, 'lng':lng, 'zoom':zoom, 'distance':distance}, 
            needs=fetch_needs(lat, lng))
    else:
        return render_template(
            'select_zone.html',
            context={'key':__credentials['api_key']}, 
        )

@app.route('/need')
def need():
    return render_template('need.html',context={'key':__credentials['api_key']})


@app.route('/add_group')
def add_group():
    return render_template('add_group.html',context={'key':__credentials['api_key']})


@app.route('/need_detail', methods=['GET'])
def need_detail():
    hash = request.args.get('h')
    need = fetch_need(hash)
    return render_template('need_detail.html', need = need, context={'key':__credentials['api_key']}, )

@app.route('/stored_enroll', methods=['POST'])
def stored_enroll_form():
    email = request.form['email']
    phone = request.form['phone']
    comment = request.form['comment']
    need_hash = request.form['need_hash']
    store_enroll(email, phone, comment, need_hash)
    return 'OK'


@app.route('/stored_need', methods=['POST'])
def stored_need_form():
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    email = request.form['email']
    title = request.form['title']
    description = request.form['description']
    type = request.form['type']
    store_need(email, lat, lng, title, description, type)
    return render_template(
        'need_detail.html', need = {
            'lat':lat,
            'lng':lng,
            'title':title,
            'description':description,
            'type':type,
            'status':'toconfirm',
            'timestamp': datetime.datetime.now(),
        },
        context={'key':__credentials['api_key']}
    )


@app.route('/group/<hash>')
def group(hash):
    group = fetch_group(hash)
    return render_template('group.html', group = group, context={'key':__credentials['api_key']}, )


@app.route('/stored_group', methods=['POST'])
def store_group_form():
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    email = request.form['email']
    name = request.form['name']
    description = request.form['description']
    url = request.form['url']
    store_group(name, description, url, lat, lng, email)
    return render_template(
        'group.html', group = {
            'lat':lat,
            'lng':lng,
            'description':description,
            'status':'toconfirm',
            'timestamp': datetime.datetime.now(),
        },
        context={'key':__credentials['api_key']}
    )



@app.route('/select_zone', methods=['GET'])
def select_zone():
    return render_template(
        'select_zone.html',
        context={'key':__credentials['api_key']}
    )


@app.route('/enable', methods=['GET'])
def enable():
    hash = request.args.get('h')
    p_hash = request.args.get('p')
    need = fetch_need(hash)
    #if (need['p_hash'] == p_hash)
    change_need_status(need.key, 'enabled')
    return('done')


@app.route('/disable', methods=['GET'])
def disable():
    hash = request.args.get('h')
    p_hash = request.args.get('p')
    need = fetch_need(hash)
    #if (need['p_hash'] == p_hash)
    change_need_status(need.key, 'disabled')
    return('done')


@app.route('/support_us', methods=['GET'])
def suport_us():
    return render_template('support_us.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
