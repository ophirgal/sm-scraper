import sys
import csv
import datetime
from decimal import Decimal
import json
from flask import Flask, request, Response, render_template
import psycopg2 as pg  # use this package to work with postgresql
import argparse

app = Flask(__name__)
conn = None


def main(argv):
    global conn


@ app.route('/')
def render_page():
    return render_template("index.html")

def get_query(fields, params):
    def list_to_sqllist(list):
        string = "("
        for word in list:
            string += "'" + word.strip() + "',"
        string = string[:-1] + ")"
        return string
    
    # prepare optional sources string
    source_query = ""
    if params.get('sources') and params.get('sources') != "":
        # select only source matches
        sources = params.get('sources').split(",")
        source_list_string = list_to_sqllist(sources)
        source_query = "AND scraped_data.subplatform in {}".format(source_list_string)

    if params.get('keywords') == "" and params.get('jurisdictions') == "":
        # maybe select all posts
        query = """
            SELECT {} FROM scraped_data 
            WHERE time_posted >= '{}' AND time_posted <= '{}' {};
            """.format(fields, params.get('dateMin'), params.get('dateMax'), source_query)
    else:
        # filter on keywords and/or jurisdictions
        keywords = params.get('keywords').split(",")
        jurisdictions = params.get('jurisdictions').split(",")
        keyword_list_string = list_to_sqllist(keywords)
        jurisdiction_list_string = list_to_sqllist(jurisdictions)

        select_query = """
            SELECT {} FROM scraped_data 
            INNER JOIN filtered_ids ON scraped_data.id = filtered_ids.id
            WHERE time_posted >= '{}' AND time_posted <= '{}' {}
                """.format(fields, params.get('dateMin'), params.get('dateMax'), source_query)

        if len(params.get('keywords')) == 0:
            # select only jurisdiction matches + sources (if applicable)
            query = """
                WITH 
                filtered_ids (id) AS 
                (SELECT DISTINCT id 
                FROM entities 
                WHERE type = 'GPE' AND entity in {})
                {};
                """.format(jurisdiction_list_string, select_query)
        elif len(params.get('jurisdictions')) == 0:
            # select only keyword matches + sources (if applicable)
            query = """
                WITH 
                filtered_ids (id) AS 
                (SELECT DISTINCT id 
                FROM key_words 
                WHERE key_word in {})
                {};
                """.format(keyword_list_string, select_query)
        else:
            # select only keyword && jurisdiction matches + sources (if applicable)
            query = """
                WITH 
                ids_from_keywords (id) AS 
                (SELECT DISTINCT id 
                FROM key_words 
                WHERE key_word in {}),

                ids_from_jurisdictions (id) AS 
                (SELECT DISTINCT id 
                FROM entities 
                WHERE type = 'GPE' AND entity in {}),

                filtered_ids (id) AS
                (SELECT DISTINCT ids_from_keywords.id 
                FROM ids_from_keywords 
                INNER JOIN ids_from_jurisdictions ON ids_from_keywords.id = ids_from_jurisdictions.id)
                {};
                """.format(keyword_list_string, jurisdiction_list_string, select_query)
    return query

@ app.route('/get-posts')
def get_posts():
    #thisState = request.args.get('reqState')

    cur = conn.cursor()

    # get posts
    #query = f'select * from scraped_data ' + getFilterSubstring(request.args) + ';'
    query = get_query("*", request.args)
    # print(query)
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
            'body': p[7], 
            'author': p[8], 
            'post_url': p[9],
            'linked_urls': "",
            'comment_count': p[10],
            'rating': "-1"
        })

    jsonData = {'postList': postList}
    resp = Response(response=json.dumps(jsonData),
                    status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = "*"
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
    relevance_threshold = 3  # TODO: change this? (arbitrary threshold)
    filtered_posts = get_query("*", request.args)[::-1].replace(';','',1)[::-1]

    # get total posts selected
    query = f'select count(*) from ({filtered_posts}) x;'
    cur.execute(query)
    posts_selected = int(cur.fetchone()[0])
    
    # get total users selected
    query = f'select count(distinct(author)) from \
        ({filtered_posts}) x;'
    cur.execute(query)
    users_selected = int(cur.fetchone()[0])
    
    # get total posts scraped
    query = f'select count(*) from scraped_data;'
    cur.execute(query)
    posts_scraped = int(cur.fetchone()[0])

    # get total posts relevant
    query = f'select count(*) from scraped_data \
        where cast(relevance_score as int) >= {relevance_threshold};'
    cur.execute(query)
    posts_relevant = int(cur.fetchone()[0])

    data = {
        'posts_selected': posts_selected,
        'users_selected': users_selected,
        'posts_scraped': posts_scraped,
        'posts_relevant': posts_relevant
    }
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
    resolution = request.args.get('resolution')
    interval_dict = {
        '1D':"('2000-01-02'::timestamp - '2000-01-01'::timestamp)",
        '1W':"('2000-01-08'::timestamp - '2000-01-01'::timestamp)",
        '1M':"('2000-02-01'::timestamp - '2000-01-01'::timestamp)",
        '3M':"('2000-04-01'::timestamp - '2000-01-01'::timestamp)",
        '1Y':"('2001-01-01'::timestamp - '2000-01-01'::timestamp)",
    }
    filtered_posts = get_query("*", request.args)[::-1].replace(';','',1)[::-1]

    # assuming client-side validation of inputs

    cur = conn.cursor()
    casted_min_date = f"'{min_date}'::timestamp"
    casted_max_date = f"'{max_date}'::timestamp"
    # bin_size = f'(({casted_max_date}-{casted_min_date}) / {total_bins})'
    bin_size = interval_dict[resolution]
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
            from ({filtered_posts}) y \
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
    word_type = request.args.get('type')

    cur = conn.cursor()
    filtered_posts = get_query("scraped_data.id", request.args)[::-1].replace(';','',1)[::-1]
    # get total posts relevant
    query = f' \
        with s(id) as ({filtered_posts}) \
        select key_word, sum(count) as count from key_words k \
        inner join s on s.id = k.id \
        group by key_word \
        order by count;' if word_type == 'words' else \
            f'with s(id) as ({filtered_posts}) \
            select entity, sum(count) as count from entities e \
            inner join s on s.id = e.id \
            group by entity \
            order by count;'
    cur.execute(query)
    data = [{'word': str(d[0]), 'count': int(d[1])}
            for d in cur.fetchall()]
   
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

    app.run(host='0.0.0.0', debug=True, port=5000)
