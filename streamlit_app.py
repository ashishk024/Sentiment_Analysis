import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import streamlit as st

# Function to clean a tweet
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

# Function to determine sentiment
def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

# Function to fetch and analyze tweets
def get_tweets(api, query, count=5):
    count = int(count)
    tweets = []
    try:
        fetched_tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items(count)
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
        st.write("Error : " + str(e))

# Streamlit UI
st.title("Twitter Sentiment Analysis")

option = st.selectbox("Select an option:", ["Phrase Level Analysis", "Sentence Level Analysis"])

if option == "Phrase Level Analysis":
    st.write("Enter a query and the number of tweets you want to analyze:")
    query = st.text_input("Query:")
    count = st.number_input("Number of Tweets:", min_value=1, max_value=100, value=5)
    if st.button("Analyze"):
        fetched_tweets = get_tweets(api, query, count)
        for tweet in fetched_tweets:
            st.write(f"Tweet: {tweet['text']}")
            st.write(f"Sentiment: {tweet['sentiment']}")
else:
    st.write("Enter a sentence for sentiment analysis:")
    text = st.text_input("Sentence:")
    if st.button("Analyze"):
        blob = TextBlob(text)
        if blob.sentiment.polarity > 0:
            text_sentiment = "positive"
        elif blob.sentiment.polarity == 0:
            text_sentiment = "neutral"
        else:
            text_sentiment = "negative"
        st.write(f"Sentiment of the sentence: {text_sentiment}")
