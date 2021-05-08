import json, datetime, time, pytz, re, sys,traceback, pymongo, sys, traceback, logging, os, re, datetime, requests, ssl
from pymongo import MongoClient

def parse(s):
    res = []
    for i in range(len(s)):
        if s[i - 4 : i] == "マンガは":
            i += 1
            while True:
                j = i
                end = False
                while s[j] != '\n':
                    j += 1
                    if j == len(s):
                        end = True
                        break
                if end : break                
                res.append(s[i : j])
                i = j + 1
                if s[i : i + 3] == "でした":
                    break
    return res

connect = MongoClient('localhost', 27017)
db = connect.mangas
tweetdata = db.tweet
meta = db.meta

find = tweetdata.find()



for i in range(find.count()):
    # print(find[i]['full_text'])
    print(parse(find[i]['full_text']))