import praw
import datetime
import os
import pandas as pd 
import numpy as np 
import time
import datetime

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
    
    def scrape(self, freq=1, limit=10, subreddits=['police', 'SocialJusticeInAction', 'Bad_Cop_No_Donut', 'BLM']):
        if not os.path.isdir('./subreddit_post'):
            os.mkdir('./subreddit_post')
        subreddit_dirs = os.listdir('./subreddit_posts')
        for subreddit in subreddits:
            if subreddit not in subreddit_dirs:
                os.mkdir('./subreddit_posts/' + subreddit)
        while True:
            for subreddit in subreddits:
                hotPosts = reddit.subreddit(subreddit).hot(limit=limit)
                for i, post in enumerate(hotPosts):
                    self.write_post(i, subreddit, post)
            time.sleep(freq * 60)

    def write_post(self, hot_rank, subreddit, post):
        post_dirs = os.listdir('./subreddit_posts/' + subreddit)
        if post.id not in post_dirs:
            os.mkdir('./subreddit_posts/' + subreddit + "/" + post.id)
            os.mkdir('./subreddit_posts/' + subreddit + "/" + post.id + "/comments")
            file = open('./subreddit_posts/' + subreddit + "/" + post.id + "/post", "w+")
            file.write("Title: " + post.title + "\n\n")
            file.write("Time created: " + str(post.created) + "\n\n")
            file.write("Author: " + str(post.author)+ ", ID: " + str(post.author.id) + "\n\n")
            file.write("URL: " + post.url + "\n\n")
            file.write("Text contents: \n" + post.selftext + "\n\n")
            file.write(str(datetime.datetime.now()) + " hotest " + str(hot_rank) + "\n")
        else:
            file = open('./subreddit_posts/' + subreddit + "/" + post.id + "/post", "a")
            file.write(str(datetime.datetime.now()) + " hotest " + str(hot_rank) + "\n")

        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            comment_files = os.listdir('./subreddit_posts/' + subreddit + "/" + post.id + "/comments")
            if comment.id not in comment_files:
                file = open('./subreddit_posts/' + subreddit + "/" + post.id + "/comments/" + comment.id, "w+")
                file.write("Time created: " + str(comment.created) + "\n\n")
                if comment.author is not None:
                    file.write("Author: " + str(comment.author) + "\n\n")
                    # file.write("Author: " + str(comment.author))
                    # if comment.author.id is not None:
                    #     file.write(", ID: " + str(comment.author.id) + "\n\n")
                    # else:
                    #     print("no ID")
                    #     file.write(", ID: no ID\n\n")
                else:
                    file.write("Author: no author\n\n")
                file.write("Text contents: \n" + comment.body + "\n\n")
        



