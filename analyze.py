#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import json
import re
import string
import time
from operator import itemgetter

punctRegex = '[^A-Za-z\'#@]+'
webAddrRegex = 'http.*?(\s|$)'

def analyze():
    with open('config.json', encoding='utf8') as configFile:
        config = json.load(configFile)
        user_name = config['targetuser']

    tweetsFile = user_name + '_tweets.json'
    with open (tweetsFile, encoding='utf8') as tweetsJson:
        alltweets = json.load(tweetsJson)

    wordDict = {}
    for tweetID in alltweets:
        text = alltweets[tweetID]['text']
        if 'http' in text:
            #print(text)
            text = re.sub(webAddrRegex, ' ', text)
            #print(text)
        text = re.sub(punctRegex, ' ', text)
        text = text.replace('#', ' #')
        text = text.replace('@', ' @')
        text= text.lower()
        text = text.split(' ')

        for word in text:
            while len(word) > 0:
                if word[0] == '\'':
                    word = word[1:]
                elif word[-1] == '\'':
                    word = word[:-1]
                elif word[0] == '#' or word[0] == '@':
                    word = ''
                elif word[-2:] == '\'s':
                    word = word[:-2]
                else:
                    if word in wordDict:
                        wordDict[word] += 1
                    else:
                        wordDict[word] = 1
                    word = ''


    fileName = user_name + '_wordcount.json'
    with open(fileName, 'w+', encoding='utf8') as outfile:
        json.dump(wordDict, outfile, ensure_ascii=False, indent='\t',sort_keys=True)


if __name__ == '__main__':
    analyze()
