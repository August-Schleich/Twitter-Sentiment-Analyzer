from matplotlib.colors import Normalize
from tweepy import OAuthHandler 
import twitter_credentials 
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt
from tweepy import api

import re
import numpy as np 
import pandas as pd 
# from tweepy import Cursor

ACCESS_TOKEN = '4827385484-U0eHiSvlT0yIRI2vMiNfwBsflJcJDON7XHOzrMU'
ACCESS_TOKEN_SECRET = 'zsc2JTzMRd9b2PXQ3UpHD9v6QmRy7mWmCbxjs6m5YVGcN'
CONSUMER_KEY = '33MsiuWcUONf3KMwr0nbZkxPe'
CONSUMER_SECRETE = 'HEVLR4VrICpeKjHBIr8HpTFafelwnqeqNtrrsQLmQEjm34Sevo'

def percentage(part,whole):
    return 100 * float(part)/float(whole)


    
   
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRETE)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
api= tweepy.API(auth,wait_on_rate_limit=True)



    

search_term =input("Enter Keyword/Hashtag to search: ")
# noOfSearchTerms= int(input("Enter how many tweets to analyze: "))

tweets = tweepy.Cursor(api.search, q=search_term, lang='en', since= '2021-11-05', tweet_mode='extended').items(200)

# store tweets in variable

all_tweets = [tweet.full_text for tweet in tweets]

df = pd.DataFrame(all_tweets, columns=['Tweets'])

#show first five rows of dataFrame

# print(df.head(5))


# function to Clean Tweets from Garbage text

def cleantwt(twt):
    twt = re.sub('#bitcoin', 'bitcoin', twt)  # Removes hashtag
    twt = re.sub('#Bitcoin', 'Bitcoin', twt)  # Removes hashtag
    twt = re.sub('#[A-Za-z0-9]+', '', twt)  # Removes any string with a '#'
    twt = re.sub('\\n', '' , twt) # Removes \n string
    twt = re.sub('https?:\/\/\S+', '' , twt) # Removes Hyperlinks
    
    return twt

# Clean tweets

df['Tweets'] = df['Tweets'].apply(cleantwt)


def getSubjectivity(twt):
    return TextBlob(twt).sentiment.subjectivity 

def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity

df['subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['polarity'] = df['Tweets'].apply(getPolarity)



def getSentiment(score):
    if score < 0:
        return "Negative"
    elif score > 0:
        return "Neutral"
    else:
        return "Positive"
    

#creat Text Column for
df['sentiment'] = df['polarity'].apply(getSentiment)



#show data column
# print(df.head(10))




#visualize DataFrame
# plt.figure(figsize=(8,6))
# for i in range(0,df.shape[0]):
#         plt.scatter(df['polarity'][i], df['subjectivity'][i], color='m')
# plt.title('Sentiment Anlysis of Search term')
# plt.xlabel('Polarity')
# plt.ylabel('Subjectivity (objective -> subjective')
# plt.show()


# Create Bar chart top show positive and negative sentiment



plt.figure(figsize=(10,8))
for i in range(0,df.shape[0]):
    df['sentiment'].value_counts().plot(kind='bar')       
plt.title('Sentiment Analysis of Bitcoin')
plt.xlabel('Sentiment')
plt.ylabel('Number of Tweets')
plt.tight_layout()
plt.show()