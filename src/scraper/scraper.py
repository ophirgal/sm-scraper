import praw
import datetime
import os
import pandas as pd 
import numpy as np 
import time
import datetime
import psycopg2

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
    
    def getConnection(self, databaseName='smsdatabase'):
        connection = psycopg2.connect(user="cmsc828d",
                                        password="cmsc828d",
                                        host="127.0.0.1",
                                        port="5432",
                                        database=databaseName)
        return connection
    
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
            for subreddit in subreddits:
                hotPosts = reddit.subreddit(subreddit).hot(limit=limit)
                for i, post in enumerate(hotPosts):
                    self.write_post_to_db(i, subreddit, post)
            time.sleep(freq * 60)

    def write_post_to_db(self, hot_rank, subreddit, post):
        connection  = self.getConnection()
        cursor = connection.cursor()

        row = [post.id,'1','reddit',subreddit,datetime.datetime.fromtimestamp(post.created),datetime.datetime.now(),post.title
        ,post.title,post.selftext,post.selftext,post.author.id,post.url,len(post.comments.list())]
        cursor.execute(
                '''INSERT INTO scraped_data VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s,%s,%s) ON Conflict(id) DO \
                   UPDATE SET "time_scraped" = EXCLUDED.time_scraped, "comment_count" = EXCLUDED.comment_count ''',
                row)
        connection.commit()



