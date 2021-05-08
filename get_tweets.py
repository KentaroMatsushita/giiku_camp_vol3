import sys
import numpy as np
import tweepy
import datetime
from requests_oauthlib import OAuth1Session
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
import json, datetime, time, pytz, re, sys,traceback, pymongo, sys, traceback, logging, os, re, datetime, requests, ssl
from pymongo import MongoClient
from collections import defaultdict

consumer_key =
consumer_secret = 
access_token = 
access_secret =

def get_last_id():
    for d in tweetdata.find({},{'id':1, 'created_at':1}).sort([{'id',pymongo.DESCENDING}]).limit(1):
        if d is not None:
            return d['id']
    return -1

def prev_day(date):
    return date - datetime.timedelta(days = 1)

def date_to_str(date):
    return date.strftime('%Y-%m-%d')

def now_unix_time():
    return time.mktime(datetime.datetime.now().timetuple())

def get_tweet(keyword, file, date):
    keyword = keyword + ' -filter:retweets' + ' since:' + date + '_00:00:00_JST' + ' until:' + date + '_23:59:59_JST'
    url = 'https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended' 
    twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_secret)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    

    api = tweepy.API(auth, wait_on_rate_limit = True)

    params ={
        'q'    : keyword,       # 検索キーワード
        'lang' : 'ja',          # 日本語のみ
        'count' : '200',     # 取得するtweet数
    }

    req = twitter.get(url, params = params)
    
    if req.status_code == 200: # 成功した場合
        timeline = json.loads(req.text)
        f = open(file, 'w')
        f.write(req.text)
        metadata = timeline['search_metadata']
        statuses = timeline['statuses']
        limit = req.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in req.headers else 0
        reset = req.headers['x-rate-limit-reset'] if 'x-rate-limit-reset' in req.headers else 0              
        return {'result':True, 'metadata':metadata, 'statuses':statuses, 'limit':limit, 'reset_time':datetime.datetime.fromtimestamp(float(reset)), 'reset_time_unix':reset}
    else:
        print('Error: %d' % req.status_code)
        print(req.text)
        return {'result':False, 'status_code':req.status_code}
    

if __name__ == '__main__':
    keyword = '#私を構成する5つのマンガ'
    file = 'data.json'
    
    connect = MongoClient('localhost', 27017)
    db = connect.mangas
    tweetdata = db.tweet
    meta = db.meta
    
    num, max_num = 0, 200
    
    date = datetime.date.today()
    while num < max_num:
        res = get_tweet(keyword, file, date_to_str(date))
        
        if res['result'] == True:
            meta.insert_one({'metadata':res['metadata'], 'insert_date': now_unix_time()})
            for s in res['statuses']:
                tweetdata.insert_one(s)
        print(date, len(res['statuses']))
        date = prev_day(date)
        num += len(res['statuses'])


    