import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer

from flask import Flask, render_template , redirect, url_for, request



def clean_tweet( tweet): 

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
         
def get_tweet_sentiment( tweet): 
        
        # analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer()) 

        # if analysis.sentiment.classification == "pos": 
        #     return 'positive'
        # elif analysis.sentiment.classification == "neg": 
        #     return 'negative'

        analysis = TextBlob(clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"


def get_tweets(api, query, count=5): 
        
        count = int(count)
        tweets = [] 
        try: 
            
            fetched_tweets = tweepy.Cursor(api.search_tweets, q=query, lang ='en', tweet_mode='extended').items(count)
            
            for tweet in fetched_tweets: 
                
                parsed_tweet = {} 

                if 'retweeted_status' in dir(tweet):
                    parsed_tweet['text'] = tweet.retweeted_status.full_text
                else:
                    parsed_tweet['text'] = tweet.full_text

                parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text']) 

                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
        except tweepy.TweepyException as e: 
            print("Error : " + str(e)) 

