import praw
import datetime
import os
import pandas as pd 
import numpy as np 
import time
import datetime
import psycopg2
import requests
import json
import collections
import argparse

reddit = praw.Reddit(
    client_id='GrsVdaeNmOR9OQ', 
    client_secret='8BcACHQ1GYERv1FlMeWwF5MH0vaUXQ',
    password="oobaka@Reddit7",
    user_agent="testscript by u/JobQuick735",
    username="JobQuick735",
)

class Scraper:
    def __init__(self,
        client_id='GrsVdaeNmOR9OQ', 
        client_secret='8BcACHQ1GYERv1FlMeWwF5MH0vaUXQ', 
        password="oobaka@Reddit7", 
        user_agent="testscript by u/JobQuick735", 
        username="JobQuick735",
        db_host='172.28.0.9',
        nlp_host='172.28.0.2'):
        self.reddit = praw.Reddit(
            client_id=client_id, 
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username,
        )
        self.db_host = db_host
        self.nlp_host = nlp_host
    
    def getConnection(self, databaseName='smscraper'):
        connection = psycopg2.connect(user="postgres",
                                        host=self.db_host,
                                        port="5432",
                                        database=databaseName)
        return connection
    
    def getLemmatized(self,text):
        response = requests.get(
            url=f'http://{self.nlp_host}:9001/get-lemma',
            params={
            'text': text,
            },
        )
        return response.json()

    def get_relevance_score(self,text, classifier= 'has_police'):
        response = requests.get(
            url = f'http://{self.nlp_host}:9001/get-relevance',
            params ={
            'text': text,
            'classifier':classifier,
            'metadata': json.dumps({}),
            },
        )
        return response.json()

    def get_entities(self, text):
        response = requests.get(
            url=f'http://{self.nlp_host}:9001/get-entities',
            params={
                'text': text,
            },
        )
        return response.json()

    def scrape(self, freq=1, limit=100000, subreddits=['police', 'SocialJusticeInAction', 'Bad_Cop_No_Donut', 'BLM']):
        connection  = self.getConnection()
        cursor = connection.cursor()
        SQL_Query = ''' CREATE TABLE IF NOT EXISTS scraped_data(
        "id"  Text PRIMARY KEY,
	    "relevance_score"  TEXT,
        "platform" TEXT,
        "subplatform" TEXT,
        "time_posted" TEXT,
        "time_scraped" TEXT,
        "title_raw"  TEXT,
        "title_lemmatized" TEXT,
        "body_raw" TEXT,
        "body_lemmatized" TEXT,
        "author" TEXT,
        "post_url" TEXT,
        "comment_count" Int
        )'''
        cursor.execute(SQL_Query)
        connection.commit()

        SQL_Query = ''' CREATE TABLE IF NOT EXISTS key_words(
        "id"  Text,
	    "key_word" Text,
        "count" Integer,
        PRIMARY KEY (id, key_word)
        )'''
        cursor.execute(SQL_Query)
        connection.commit()

        SQL_Query = ''' CREATE TABLE IF NOT EXISTS entities(
        "id"  Text,
	    "entity" Text,
        "type" Text,
        "count" Integer,
        PRIMARY KEY (id, entity, type)
        )'''
        cursor.execute(SQL_Query)
        connection.commit()

        while True:
            print('scraping')
            for subreddit in subreddits:
                hotPosts = reddit.subreddit(subreddit).hot(limit=limit)
                for i, post in enumerate(hotPosts):
                    self.write_post_to_db(i, subreddit, post)
            time.sleep(freq * 60)

    def write_post_to_db(self, hot_rank, subreddit, post):
        connection  = self.getConnection()
        cursor = connection.cursor()
        relevenace_score_title = self.get_relevance_score(post.title)
        relevenace_score_body = self.get_relevance_score(post.selftext)
        if relevenace_score_title['relevant'] or relevenace_score_body['relevant']:
            # Get lemmatized title and body
            title_lemmatized =  self.getLemmatized(post.title)
            title_lemmatized = " ".join(title_lemmatized)
            body_lemmatized = self.getLemmatized(post.selftext)
            key_words = collections.Counter(body_lemmatized)
            cursor.execute(
                    '''DELETE FROM key_words WHERE id = %s''', [str(post.id)]
                )
            connection.commit()
            for key_word in key_words:
                row = [post.id, key_word, key_words[key_word]]
                cursor.execute(
                    '''INSERT INTO key_words VALUES (%s, %s, %s)''', row
                )
                connection.commit()

            entities = self.get_entities(post.selftext)
            entities_dict = {}
            for entity in entities:
                if (entity[0], entity[2]) in entities_dict:
                    entities_dict[(entity[0], entity[2])] += 1
                else:
                    entities_dict[(entity[0], entity[2])] = 1
            cursor.execute(
                    '''DELETE FROM entities WHERE id = %s''', [str(post.id)]
                )
            connection.commit()
            for key, value in entities_dict.items():
                row = [post.id, key[0], key[1], value]
                cursor.execute(
                    '''INSERT INTO entities VALUES (%s, %s, %s, %s)''', row
                )
                connection.commit()

            relevant_score = max(int(relevenace_score_title['score']),int(relevenace_score_body['score']))
            author_id = None
            if (post.author is not None):
                author_id = post.author.id
            row = [post.id,relevant_score,'reddit',subreddit,datetime.datetime.fromtimestamp(post.created),datetime.datetime.now(),post.title
            ,title_lemmatized,post.selftext,body_lemmatized,author_id,post.url,len(post.comments.list())]
            cursor.execute(
                    '''DELETE FROM scraped_data WHERE id = %s''', [str(post.id)]
                )
            connection.commit()
            cursor.execute(
                    '''INSERT INTO scraped_data VALUES (%s,%s, %s, %s, %s, %s,
                    %s, %s, %s,%s, %s,%s,%s)''',
                    row)
            connection.commit()

if __name__ == '__main__':	
    
    # Define and parse (optional) arguments for the script 
    parser = argparse.ArgumentParser()
    parser.add_argument('--host-os', default='mac', type=str, choices=['windows', 'mac', 'linux'])
    args = parser.parse_args()
    host_os = args.host_os
    nlp_host = 'localhost' if host_os == 'linux' else '172.28.0.2'
    db_host = 'localhost' if host_os == 'linux' else '172.28.0.9'

    scrapeObj = Scraper(nlp_host=nlp_host, db_host=db_host)
    scrapeObj.scrape()



