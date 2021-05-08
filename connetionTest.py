import sys
import numpy as np
import tweepy
import datetime
from requests_oauthlib import OAuth1Session
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
import json, datetime, time, pytz, re, sys,traceback, pymongo
from pymongo import MongoClient
from collections import defaultdict

consumer_key = '8W9ptTr4e0l6UzojsE4CWYKz8'
consumer_secret = 'Vb3usdlFhAGzBgNoKF2F8JnBVj0dhPBi31nVuYpl6LkvmkaiS8'
access_token = '1193915851931451392-4NtXrufuwnmMpRMmkcbTY8qTJnjHXR'
access_secret = 'gHtvZ9Acvto7v08IOjyHnp12z4saMW2rn55lV94qWpk6s'


def get_tweet(keyword, file):
    url = 'https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended' 
    twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_secret)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    connect = MongoClient('localhost', 27017)
    db = connect.test
    meta = connect.test2

    api = tweepy.API(auth, wait_on_rate_limit = True)

    params = {
        'a' : keyword,
        'count' : 2,
    }

    req = twitter.get(url, params = params)
    
    if req.status_code == 200: # 成功した場合
        timeline = json.loads(req.text)
        f = open(file, 'w')
        f.write(timeline)
        metadata = timeline['search_metadata']
        statuses = timeline['statuses']
        limit = req.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in req.headers else 0
        reset = req.headers['x-rate-limit-reset'] if 'x-rate-limit-reset' in req.headers else 0              
        return {'result':True, 'metadata':metadata, 'statuses':statuses, 'limit':limit, 'reset_time':datetime.datetime.fromtimestamp(float(reset)), 'reset_time_unix':reset}
    else:
        print('Error: %d' % req.status_code)
        return {'result':False, 'status_code':req.status_code}
    

if __name__ == '__main__':
    keyword = '中日ドラゴンズ'
    file = 'data.json'
    res = get_tweet(keyword, file)
    
    if res['result'] == True:
        meta.insert_one({'metadata':res['metadata'], 'insert_date': now_unix_time()})
        for s in res['statuses']:
            tweetdata.insert_one(s)
        print('done')

    