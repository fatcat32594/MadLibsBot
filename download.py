#!/usr/bin/env python
# encoding: utf-8

import tweepy
import json
import time
import os.path

def get_all_tweets():
    #get configuration
    with open('config.json', 'r') as configFile:
        config = json.load(configFile)
        screen_name = config['targetuser']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        access_key = config['access_key']
        access_secret = config['access_secret']

    fileName = screen_name + '_tweets.json'

    #read old data, if exists
    if os.path.exists(fileName):
        with open(fileName, 'r', encoding='utf8') as infile:
            outtweets = json.load(infile)
            sinceID = max(outtweets)
            print(sinceID)
    else:
        outtweets = {}
        sinceID = 0

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=20, since=sinceID)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = screen_name,count=20,since = sinceID, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

    for tweet in alltweets:
        outtweets[tweet.id_str] = {"date": str(tweet.created_at), "text": tweet.text}

    if len(alltweets) > 0:
        with open(fileName, 'w+', encoding='utf8') as outfile:
            json.dump(outtweets, outfile, ensure_ascii=False, indent='\t',sort_keys=True)


if __name__ == '__main__':
    get_all_tweets()
