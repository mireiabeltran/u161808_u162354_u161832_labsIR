import datetime
from random import random

from faker import Faker
import json


fake = Faker()



# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


class Document:
    def __init__(self, id, title, description, likes, retweets, date):
        self.id = id
        self.title = title
        self.description = description
        self.likes = likes
        self.retweets = retweets
        self.date = date


def load_documents_corpus():
    """
    Load documents corpus from dataset_tweets_WHO.txt file
    :return:
    """
    text = open('/Users/ciscoorteu/Desktop/UNI/4rt/1T/Web Retrival/search-engine-web-app-main/search-engine-web-app-main/app/core/dataset_tweets_WHO.txt', 'r')
    ##### demo replace ith your code here #####
    
    for line in text:
        tweet=json.loads(line)
    
    tweets_data_=[]
    for i in range(len(tweet)):
        tweet_id = tweet[str(i)]['id']
        tweet_title = tweet[str(i)]['full_text'][:67]
        tweet_text = tweet[str(i)]['full_text']
        t_ret = tweet[str(i)]['retweet_count']
        t_likes = tweet[str(i)]['favorite_count']
        t_date = tweet[str(i)]['created_at']
        tweets_data_.append(Document(tweet_id, tweet_title, tweet_text, t_likes, t_ret, t_date))
    text.close()


    return tweets_data_
    
    
