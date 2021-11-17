
from matplotlib.colors import Normalize
from tweepy import OAuthHandler 
import twitter_credentials 
from textblob import TextBlob
import sys, tweepy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from tweepy import api
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



    

searchTerm =input("Enter Keyword/Hashtag to search: ")
noOfSearchTerms= int(input("Enter how many tweets to analyze: "))

tweets = tweepy.Cursor(api.search, q=searchTerm, lang='English',tweet_mode='extended').items(10)

positive = 0

negative = 0

neutral = 0 

polarity = 0

for tweet in tweets:
    print(tweet.full_text)
    analysis = TextBlob(tweet.full_text)
    polarity += analysis.sentiment.polarity
    if (analysis.sentiment.polarity ==0):
        neutral += 1
    elif (analysis.sentiment.polarity < 0):
        negative += 1
    elif (analysis.sentiment.polarity >0):
        positive += 1
 

positive = percentage(positive, noOfSearchTerms)

negative = percentage(negative, noOfSearchTerms)

neutral = percentage(neutral, noOfSearchTerms)

polarity = percentage(polarity, noOfSearchTerms)

positive = format(positive, '.2f')

neutral = format(neutral, '.2f')

negative = format(negative, '.2f')


print("how people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + 'Tweets.')

if (polarity ==0):
    print('Neutral')
elif(polarity > 0):
    print('Positive')
elif(polarity < 0):
    print("Negative")




labels= ['Positive [' + str(positive)+'%]','Neutral [' + str(neutral)+'%]','Negative [' + str(negative)+'%]']

sizes = [positive, neutral, negative, ]

colors = ['m', 'gold','red']

patches, texts = plt.pie(sizes, colors=colors, startangle=90)

plt.legend(patches,labels, loc="best")
plt.suptitle("how people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + '  Tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show
