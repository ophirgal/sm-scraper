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

def getFilterSubstring(params):
    return "WHERE \"time_posted\" >= '{}' AND \"time_posted\" <= '{}'".format(params.get('dateMin'), params.get('dateMax'))

@ app.route('/get-posts')
def get_data():
    #thisState = request.args.get('reqState')

    cur = conn.cursor()

    # get posts
    query = f'select * from scraped_data ' + getFilterSubstring(request.args) + ';'
    cur.execute(query)
    res = cur.fetchall()

    postList = []
    for p in res:
        postList.append({ 
            'relevance_score': p[1],
            'platform': p[2],
            'subplatform': p[3],
            'time_posted': p[4],
            'time_scraped': p[5],
            'title': p[6], 
            'body': p[8], 
            'author': p[10], 
            'post_url': p[11],
            'linked_urls': "https://google.com",
            'comment_count': p[12],
            'rating': "-1"
        })

    jsonData = {'postList': postList}
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
    relevance_threshold = 3

    # get total posts scraped
    query = f'select count(*) from scraped_data;'
    cur.execute(query)
    posts_scraped = int(cur.fetchone()[0])

    # get total posts relevant
    query = f'select count(*) from scraped_data \
        where cast(relevance_score as int) >= {relevance_threshold};'
    cur.execute(query)
    posts_relevant = int(cur.fetchone()[0])

    data = {'posts_scraped': posts_scraped,
            'posts_relevant': posts_relevant}
    return _json_response(data)


@ app.route('/get-date-histogram')
def get_date_histogram():
    # # stale request handler
    # global reqState
    # thisState = int(request.args.get('reqState'))
    # if reqState != thisState:
    #     print("STALE REQ: ABORTING")
    #     return

    min_date = request.args.get('minDate')
    max_date = request.args.get('maxDate')
    total_bins = request.args.get('totalBins')

    if min_date == max_date:
        return 'Make sure date range is valid (at least one day apart).', 500

    cur = conn.cursor()
    casted_min_date = f"'{min_date}'::timestamp"
    casted_max_date = f"'{max_date}'::timestamp"
    bin_size = f'(({casted_max_date}-{casted_min_date}) / {total_bins})'
    query = \
        f'select \
        ({casted_min_date} + (bucket-1) * {bin_size}) as bin_min, \
        ({casted_min_date} + (bucket  ) * {bin_size}) as bin_max, \
        cnt from \
            (select width_bucket(time_posted::timestamp, \
                array(select generate_series( \
                    {casted_min_date}, {casted_max_date}, {bin_size}))) \
            as bucket, \
            sum(case when (time_posted::timestamp >= {casted_min_date} and \
                time_posted::timestamp <= {casted_max_date}) then 1 else 0 end) \
                     as cnt \
            from scraped_data \
            group by bucket \
            order by bucket) x;'
    cur.execute(query)
    data = [{'binMin': str(d[0]), 'binMax': str(d[1]), 'count': int(d[2])}
            for d in cur.fetchall()]
    return _json_response(data)


@ app.route('/get-word-distribution')
def get_word_distribution():
    # # stale request handler
    # global reqState
    # thisState = int(request.args.get('reqState'))
    # if reqState != thisState:
    #     print("STALE REQ: ABORTING")
    #     return


    cur = conn.cursor()
   
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
        conn = pg.connect(user="postgres",
                          host=app.config['db_host'],
                          port="5432",
                          database='smscraper')
        print('Successfully connected to the database.')
    except Exception as e:
        print(e)
        print("Unable to connect to the database!")

    flask_host = 'localhost' if 'localhost' in sys.argv else '0.0.0.0'
    app.run(host=flask_host, debug=True, port=5000)
