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

Kafka was chosen because of the ease of setup on AWS EC2. A Vagrant startup file and Ansible Zookeeper and Kafka configuration playbook are executed to create and start the Kafka server.

The Twitter stream processor listens to the Twitter Streaming API and places tweets that have geolocation data and are english language onto the Kafka topic.

### Sentiment Analysis Pipeline

Set up a worker that will consume tweets from your message broker and perform sentiment analysis using TextBlob (https://textblob.readthedocs.org/en/dev/quickstart.html#sentiment-analysis) or a similar library. We recommend using a task queueing system such as Celery (http://www.celeryproject.org/) or RQ (http://python-rq.org/) though you can also use the message broker directly. This component should be designed to scale to multiple machines easily and tolerate instance failures. The results of sentiment analysis should be stored in a MongoDB collection for retrieval from the API. See Sentiment API doc below to figure out which fields will need to be persisted.

An AWS ElasticCache backed with Redis was created for ease of creation and management, and the Python RQ library was chosen to work with it also because of its simplicity. 

A Python command line program was created to consume messages from the Kafka topic (tweets) and queue them onto an RQ queue for sentiment processing with TextBlob.

Another Python program implements the sentiment processor worker that dequeues the processing job, executes the sentiment analysis and places the results into MongoDB. The results consist of the sentiment scores, tweet text and location data.

Both of these Python programs are simple and multiples of them may be executed on machines with available cores, which allows quick horizontal scaling. However more management tooling is necessary to create larger sets of parallel processes to queue and de-queue these tasks. Currently these programs run on a t2.micro instance, one per program.

### Database

Set up a MongoDB collection with indexing to support the structure of the API response as presented below.

The MongoDB is a single instance AWS EC2 m3.large SSD instance. It isn't a large server in order to keep costs down, but is set up with SSD. A single sentiment collection contains each analyzed tweet text, sentiment scores and location document.
A geolocation 2dsphere index is created on the `location` field of the documents to allow use of MongoDB's geo-query functionality. In this way we can use an aggregation query to compute the average, min, and max sentiment scores that fall within a 2d sphere of a given radius.


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

The REST API is located at `http://develop.8hum4jfqxp.us-west-1.elasticbeanstalk.com`

A sample query is `http://develop.8hum4jfqxp.us-west-1.elasticbeanstalk.com/sentiment?lat=40.9&lon=-75.0&dist=100` which looks for tweets in a 100km radius around the geographical point given by the lat/lon coordinates.



