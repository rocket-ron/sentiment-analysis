# sentiment-analysis
Twitter sentiment analysis system

## Objective

Build and deploy a system in Python for sentiment analysis of public, geolocated social media posts.

## Components

- Twitter Streaming Consumer

- Sentiment Analysis pipeline to process tweets

- Database for storing sentiment of social updates

- RESTful API providing sentiment stats by location

### Twitter Streaming Consumer

Set up a simple consumer of the Twitter Streaming API to get a stream of all public, geolocated tweets (filter out any post without geo). Tweedy (http://tweepy.readthedocs.org/en/v3.5.0/streaming_how_to.html) is a good library for consuming the streaming API. These tweets should be dispatched to your sentiment analysis workers through a message broker like RabbitMQ, Redis, or Kafka.

### Sentiment Analysis Pipeline

Set up a worker that will consume tweets from your message broker and perform sentiment analysis using TextBlob (https://textblob.readthedocs.org/en/dev/quickstart.html#sentiment-analysis) or a similar library. We recommend using a task queueing system such as Celery (http://www.celeryproject.org/) or RQ (http://python-rq.org/) though you can also use the message broker directly. This component should be designed to scale to multiple machines easily and tolerate instance failures. The results of sentiment analysis should be stored in a MongoDB collection for retrieval from the API. See Sentiment API doc below to figure out which fields will need to be persisted.

### Database

Set up a MongoDB collection with indexing to support the structure of the API response as presented below.

### Sentiment API

Design a RESTful API with Flask (http://flask.pocoo.org/), Bottle (http://bottlepy.org/docs/dev/index.html), or a similar library that allows a user to query the average sentiment at a location by providing a latitude, longitude, and radius. The API should provide a JSON response in the following format:

    {
        "tweets": 100, // number of tweets
        "average_polarity": 0.4, // TextBlob provides a polarity value for sentiment analysis
        "most_positive": { // tweet at this location with highest polarity
            "text": “what a great day!”,
            "coordinates": [-75.14310264, 40.05701649]
        },
        "most_negative": { // tweet at this location with lowest polarity
            "text": “worst lunch ever!”,
            "coordinates": [-75.14311344, 40.05701716]
        }
    }
    
### Deployment

Project should be hosted in a public repository on Github or Bitbucket. The system should be deployed on AWS EC2, Elasticbeanstalk, Heroku, Google AppEngine, or a similar service.

