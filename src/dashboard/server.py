import sys
import csv
import datetime
from decimal import Decimal
import json
from flask import Flask, request, Response, render_template
import psycopg2 as pg  # use this package to work with postgresql
import argparse

app = Flask(__name__)
reqState = 0
conn = None


def main(argv):
    global reqState
    global conn


@ app.route('/')
def render_page():
    return render_template("index.html")


@ app.route('/get-state')
def get_state():
    global reqState
    reqState += 1
    resp = Response(response=str(reqState), status=200, mimetype='text/plain')
    return resp


@ app.route('/get-data')
def get_data():
    global reqState
    global conn
    thisState = int(request.args.get('reqState'))
    if reqState != thisState:
        print("STALE REQ: ABORTING")
        return

    cur = conn.cursor()

    jsonData = {'data': ""}
    resp = Response(response=json.dumps(jsonData),
                    status=200, mimetype='application/json')
    return resp

##########################    OPHIR'S SECTION (BEGIN)    ######################


def _json_response(data):
    resp = Response(response=json.dumps(data), status=200,
                    mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


@ app.route('/get-stats')
def get_stats():
    # # stale request handler
    # global reqState
    # thisState = int(request.args.get('reqState'))
    # if reqState != thisState:
    #     print("STALE REQ: ABORTING")
    #     return

    cur = conn.cursor()
    # get total posts selected
    query = f'select count(*) from scraped_data;'
    cur.execute(query)
    posts_selected = int(cur.fetchone()[0])
    
    # get total users selected
    query = f'select count(distinct(author)) from scraped_data;'
    cur.execute(query)
    users_selected = int(cur.fetchone()[0])
    
    # get total posts scraped
    query = f'select count(*) from scraped_data;'
    cur.execute(query)
    posts_scraped = int(cur.fetchone()[0])
    
    # get total posts relevant
    query = f'select count(*) from scraped_data;'
    cur.execute(query)
    posts_relevant = int(cur.fetchone()[0])

    data = {'posts_selected': posts_selected,
            'users_selected': users_selected, 
            'posts_scraped': posts_scraped,
            'posts_relevant': posts_relevant}
    return _json_response(data)


##########################    OPHIR'S SECTION (END)      ######################


if __name__ == "__main__":

    # Define and parse (optional) arguments for the script
    parser = argparse.ArgumentParser()
    parser.add_argument('--host-os', default='mac', type=str,
                        choices=['windows', 'mac', 'linux'])
    args = parser.parse_args()
    host_os = args.host_os
    app.config['db_host'] = 'localhost' if host_os == 'linux' else '172.28.0.9'
    app.config['nlp_host'] = 'localhost' if host_os == 'linux' else '172.28.0.2'

    # try to connect to DB
    try:
        conn = pg.connect(user="cmsc828d",
                          password="pword",
                          host=app.config['db_host'],
                          port="5432",
                          database='smscraper')
        print('Successfully connected to the database.')
    except Exception as e:
        print(e)
        print("Unable to connect to the database!")

    flask_host = 'localhost' if 'localhost' in sys.argv else '0.0.0.0'
    app.run(host=flask_host, debug=True, port=5000)
