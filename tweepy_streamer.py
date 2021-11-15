from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler 
from tweepy import Stream 

import twitter_credentials 
from textblob import TextBlob
import tweepy
import re
import numpy as np 
import pandas as pd 
#### Twitter Client #####

class TwitterClient():
    
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client
        
    def get_user_timeline_tweets(self, num_tweets):
        tweets= []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            return tweets  
    
    def get_friends_list(self,num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
            return friend_list
        
    def get_home_timeline_tweets(self,num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
            return home_timeline_tweets

   

        





##### Twitter Authenticator #####

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRETE)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth
    

class TwitterStreamer():
    """ 
    Class for streaming and processing live tweets
    """
    def __init__(self,):
        self.twitter_authenticator = TwitterAuthenticator()
        

    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list): 
       
        """
         This handles Twitter authentication and connection to the Twitter streaming API
        """
        
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
    
        stream.filter(track=hash_tag_list)
    

class TwitterListener(StreamListener):
    """
    This is a basic class that prints recieved tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
       self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e: 
            print("Error on data: %s" % str(e))   
        return True
    
    
    def on_error(self, status):
        if status== 420:
            ## checks for rate limit error to keep from getting locked out
            return False
        print(status)
        
class TweetAnalyzer():
    """
    For analysis and cotagorizing tweets 
    """

    def tweets_to_data_frame(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweets'])
     
        
        return df
    
    def clean_tweet(self,tweet):
        
         return ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        
    def analyze_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0 :
            return 0
        else:
            return -1
        
if __name__ == "__main__":
    
    hash_tag_list = ['bitcoin','cardano','ethereum']
    fetched_tweets_filename = 'tweets.json'
    
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    
    api = twitter_client.get_twitter_client_api()
     
    tweets = api.user_timeline(screen_name='',count=10)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
    df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweets'])

    print(df.head(1))

    
    # print(twitter_client.get_home_timeline_tweets(1))
    
    for i in tweets:
            print(i.text)