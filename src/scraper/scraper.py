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
        username="JobQuick735"):
        self.reddit = praw.Reddit(
            client_id=client_id, 
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username,
        )
    
    def getConnection(self, databaseName='smscraper'):
        connection = psycopg2.connect(user="cmsc828d",
                                        password="pword",
                                        host="172.28.0.9",
                                        port="5432",
                                        database=databaseName)
        return connection
    
    def getLemmatized(self,text):
        response = requests.get(
            url= 'http://172.28.0.2:9001/get-lemma',
            params={
            'text': text,
            },
        )
        return response.json()

    def get_relevance_score(self,text, classifier= 'has_police'):
        response = requests.get(
            url = 'http://172.28.0.2:9001/get-relevance',
            params ={
            'text': text,
            'classifier':classifier,
            'metadata': json.dumps({}),
            },
        )
        return response.json()

    def scrape(self, freq=1, limit=10, subreddits=['police', 'SocialJusticeInAction', 'Bad_Cop_No_Donut', 'BLM']):
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
            body_lemmatized = " ".join(body_lemmatized)
            relevant_score = max(int(relevenace_score_title['score']),int(relevenace_score_body['score']))

            row = [post.id,relevant_score,'reddit',subreddit,datetime.datetime.fromtimestamp(post.created),datetime.datetime.now(),post.title
            ,title_lemmatized,post.selftext,body_lemmatized,post.author.id,post.url,len(post.comments.list())]
            cursor.execute(
                    '''INSERT INTO scraped_data VALUES (%s,%s, %s, %s, %s, %s,
                    %s, %s, %s,%s, %s,%s,%s) ON CONFLICT (id) DO \
                    UPDATE SET time_scraped = EXCLUDED.time_scraped, \
                    comment_count = EXCLUDED.comment_count''',
                    row)
            connection.commit()
	
scrapeObj = Scraper()
scrapeObj.scrape()



