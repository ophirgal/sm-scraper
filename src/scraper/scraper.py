import time
import psycopg2
import json
import requests


i = 1
while(True):
    # make some API calls
    # ...
    # print(requests.get('https://www.ophirgal.com/').text)  # get request ex.

    # Analyze using the NLP module and add to DB
    # ...

    # sleep for a bit
    time.sleep(5)  # in seconds
    
    print('hey from scraper', i)
    i += 1
