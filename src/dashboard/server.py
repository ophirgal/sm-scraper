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

    # states = request.args.get('states')
    # statesList = states.split(",")

    cur = conn.cursor()

    if reqState != thisState:
        print("STALE REQ: ABORTING")
        return

    # Get all rows for all states
    data = []
    dataAvg = []
    i = 0

    '''
    for s in statesList:
    if reqState != thisState:
      print("STALE REQ: ABORTING")
      return
    i += 1

    cur.execute("SELECT \"submission_date\",\"{}\" FROM public.us_states_covid WHERE \"state\" = '{}' AND ((CAST('{}' AS date) - CAST(submission_date AS date)) % '{}') = 0 AND \"submission_date\" >= '{}' AND \"submission_date\" <= '{}' ORDER BY \"submission_date\" ASC;".format(attribute, s, mx, interval, mn, mx))

    res = cur.fetchall()
    thisData = []
    for d in res:
      thisData.append({'date':d[0].strftime("%Y-%m-%d"), 'val':float(d[1])})
    data.append(thisData)

    cur.execute("SELECT AVG(\"{}\") FROM public.us_states_covid WHERE \"state\" = '{}' AND ((CAST('{}' AS date) - CAST(submission_date AS date)) % '{}') = 0 AND \"submission_date\" >= '{}' AND \"submission_date\" <= '{}';".format(attribute, s, mx, interval, mn, mx))
    res = cur.fetchall()
    dataAvg.append({'state':s, 'avg':float(res[0][0])})
    '''
    if reqState != thisState:
        print("STALE REQ: ABORTING")
        return

    # prep data for delivery
    jsonData = {'data': ""}
    resp = Response(response=json.dumps(jsonData),
                    status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    host = 'localhost' if 'localhost' in sys.argv else '0.0.0.0'
    app.run(host=host, debug=True, port=5000)
