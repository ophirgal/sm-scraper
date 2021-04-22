import sys

import csv
import datetime
from decimal import Decimal
import json
from flask import Flask, request, Response, render_template
import psycopg2 as pg  # use this package to work with postgresql

app = Flask(__name__)
reqState = 0

try:
    conn = pg.connect(user="cmsc828d",
                      password="pword",
                      host="127.0.0.1",
                      port="5432",
                      database='smscraper')
    print('Successfully connected to the database.')
except:
    print("Unable to connect to the database!")


def main(argv):
    global reqState


@ app.route('/')
def renderPage():
    return render_template("index.html")


@ app.route('/get-state')
def getState():
    global reqState
    reqState += 1
    resp = Response(response=str(reqState), status=200, mimetype='text/plain')
    return resp


@ app.route('/get-data')
def getData():
    global reqState
    thisState = int(request.args.get('reqState'))
    if reqState != thisState:
        print("STALE REQ: ABORTING")
        return

    cur = conn.cursor()

    jsonData = {'data': ""}
    resp = Response(response=json.dumps(jsonData),
                    status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    host = 'localhost' if 'localhost' in sys.argv else '0.0.0.0'
    app.run(host=host, debug=True, port=5000)
