import datetime
import uuid

from flask import Flask, render_template, request
from google.cloud import datastore
import mgrs


datastore_client = datastore.Client()

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
        'status' : 'toconfirm',
        'hash': uuid.uuid4().hex,
        'p_hash': uuid.uuid4().hex
    })

    datastore_client.put(entity)

def fetch_need(hash):
    query = datastore_client.query(kind='need')
    query.add_filter('hash', '=', hash)
    needs = query.fetch(limit=1)
    for need in needs:
        return need

def fetch_needs(lat, lng):
    needs_mgrs = mgrs.MGRS().toMGRS(lat, lng).decode('UTF-8')
    query = datastore_client.query(kind='need')
    query.add_filter('status', '=', 'toconfirm')
    query.add_filter('mgrs_6', '=', needs_mgrs[:6])
    needs = query.fetch(limit=20)
    return needs


@app.route('/')
def root():
    return render_template(
        'index.html')


@app.route('/offer', methods=['GET'])
def offer():
    z = request.args.get('z')
    if z:
        lat, lng, zoom, distance = z.split(',')

        return render_template(
            'offer.html', 
            context={'key':'AIzaSyAnmtePzc5y5TgEIj9ewyBDNyRvcNFzuNw'}, 
            zone={'lat':lat, 'lng':lng, 'zoom':zoom, 'distance':distance}, 
            needs=fetch_needs(lat, lng))
    else:
        return render_template(
            'select_zone.html',
            context={'key':'AIzaSyAnmtePzc5y5TgEIj9ewyBDNyRvcNFzuNw'}, 
        )

@app.route('/need')
def need():
    return render_template('need.html',context={'key':'AIzaSyAnmtePzc5y5TgEIj9ewyBDNyRvcNFzuNw'})

@app.route('/need_detail', methods=['GET'])
def need_detail():
    hash = request.args.get('h')
    need = fetch_need(hash)
    print(need)
    return render_template('need_detail.html', need = need, context={'key':'AIzaSyAnmtePzc5y5TgEIj9ewyBDNyRvcNFzuNw'}, )

@app.route('/stored_need', methods=['POST'])
def stored_need_form():
    lat = request.form['lat']
    lng = request.form['lng']
    email = request.form['email']
    title = request.form['title']
    description = request.form['description']
    type = 'other'
    store_need(email, lat, lng, title, description, type)
    return render_template(
        'need_detail.html', need = {
            'lat':lat,
            'lng':lng,
            'title':title,
            'description':description,
            'type':type,
            'status':'toconfirm'
        },
        context={'key':'AIzaSyAnmtePzc5y5TgEIj9ewyBDNyRvcNFzuNw'}
    )


@app.route('/select_zone', methods=['GET'])
def select_zone():
    return render_template(
        'select_zone.html',
        context={'key':'AIzaSyAnmtePzc5y5TgEIj9ewyBDNyRvcNFzuNw'}
    )

@app.route('/enable', methods=['GET'])
def enable():
    return('done')

@app.route('/support_us', methods=['GET'])
def suport_us():
    return render_template('support_us.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
