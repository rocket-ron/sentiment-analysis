from textblob import TextBlob
from pymongo import MongoClient


def process_tweet(tweet, host, port, db):
    if 'text' in tweet:
        print 'processing...'
        mongo_client = MongoClient(host=host, port=port, db=db)
        mongodb = mongo_client[db]
        tweet_text_blob = TextBlob(tweet['text'])
        result = dict(text=tweet['text'],
                      coordinates=tweet['coordinates'],
                      polarity=tweet_text_blob.polarity,
                      subjectivity=tweet_text_blob.subjectivity)

        mongodb.sentiment.save(result)



