#!/usr/bin/env python
# -*- coding: utf-8 -*-
import got3 as got
def print_tweets(tweets):
    print("取得件数：", len(tweets))
    for tweet in tweets: 
        print("---------------------------------")
        print("ツイートID：", tweet.id)
        print("ツイートURL：", tweet.permalink)
        print("アカウントの文字列：", tweet.username)
        print(tweet.text)
        print("投稿日：", tweet.date)
        print("リツイート数：", tweet.retweets)
        print("いいねの数：", tweet.favorites)
        if tweet.mentions: 
            print("メンションの内容：", tweet.mentions)
        if tweet.hashtags:
            print("ハッシュタグの内容", tweet.hashtags)

# アカウントの文字列で取得
tweetCriteria = got.manager.TweetCriteria().setUsername("sugoiyamanaka").setMaxTweets(5)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
print("---------------------------------")
print("①アカウントの文字列で取得")
print_tweets(tweets)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

print(tweet.text)