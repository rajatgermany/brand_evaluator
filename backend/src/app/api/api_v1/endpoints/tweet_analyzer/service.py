import numpy as np
import pandas as pd
import tweepy

from app.core.session import SessionData
from app.ml_model_2 import get_sentiment, most_frequent_words
from app.db_models.tweet import Tweet
from app.db.session import db_session
from app.preprocessing import Preprocessing
from app.core import config

preprocessing = Preprocessing()
session = SessionData()

class TwitterTweetAnalyzer:
    """Proxy Service between model and router handler. It handles preprocessing and post-proprocessing 
    """
    def __init__(self, query):
        self.api = self.intialize_twitter_api()
        self.query = query
        self.fetched_tweets = []

    def intialize_twitter_api(self):
        """Intializes the tweepy objecr
        
        Returns:
            [type] -- Twitter Tweepy object
        """
        
        API_KEY = config.API_KEY
        API_SECRET_KEY = config.API_SECRET_KEY
        ACCESS_TOEKN = config.ACCESS_TOEKN
        ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET
        auth  = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOEKN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)   
        return api 

    def download_tweets(self):
        self.fetched_tweets = self.api.search(q = self.query,  lang="en", since="2017-04-03")
        return self.fetched_tweets

    def preprocess_tweets(self):
        tweets = []
        for tweet in self.fetched_tweets: 
            cleaned_tweet_text = preprocessing.clean_tweet_text(tweet.text)
            setattr(tweet, 'text', cleaned_tweet_text)
            tokenized_tweet_text = preprocessing.tokenize_tweet_text(tweet.text)
            setattr(tweet, 'tokenized_tweet_text', tokenized_tweet_text)
            tweets.append(tweet)
        self.fetched_tweets = tweets
        return self.fetched_tweets

    def add_sentiment_to_tweeets(self):
        tweets = []
        for tweet in self.fetched_tweets: 
            tweet_sentiment = get_sentiment(tweet.tokenized_tweet_text)
            setattr(tweet, 'sentiment', tweet_sentiment)
            tweets.append(tweet)
        self.fetched_tweets = tweets

    def normalize_tweets(self):
        return [{
            'text': tweet.text,
            'sentiment': 'Positive' if tweet.sentiment == 1 else 'Negative',
            "created_at": str(tweet.created_at),
            "frequent_words": self.frequent_words,
            "user_location": tweet.user.location,
            "retweet_count": tweet.retweet_count,
            "favorite_count": tweet.favorite_count
        } for tweet in self.fetched_tweets]


    def add_most_frequent_words(self):
        frequent_words = most_frequent_words(self.fetched_tweets)
        self.frequent_words = frequent_words.most_common(15)
        