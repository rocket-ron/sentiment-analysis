# Twitter Stream Processors

There are 3 components in the Twitter stream processing:

- The Twitter stream listener, which registers for the Twitter stream and places tweets in a Kafka topic

- The Kafka consumer, which takes each tweet off the Kafka topic and queues the sentiment processor job for the tweet

- The Sentiment processor, which measures the tweet sentiment polarity and subjectivity scores and writes the results to MongoDB

## Twitter Stream Listener

The Twitter stream listener is a simple Python program that uses a single Twitter API key to register as a streaming API consumer. The program runs from the command line with command line arguments
to specify the Twitter API key, the type of stream events if which we're interested such as tracking or location, and the Kafka connection information.

The stream listener registers for tweets that contain location data and are english language tweets. However, not all tweets meet this criteria that are intercepted by the stream listener so additional
program checks are made to take only those tweets that have geolocation data and have an english language specification. Once those criteria are met the tweet is placed in the Kafka topic.

## Kafka Tweet Consumer

The Kafka tweet consumer is a simple Python program that registers to consume messages from the 'tweets' topic of the Kafka server. For every tweet consumed from the topic a job is scheduled on a Python RQ
task queue. This allows decoupling of the execution of the sentiment analysis and storing of the results in MongoDB from the tweet stream consumption.

## Sentiment Processor

The Python RQ task executes on a simple worker program that executes the sentiment analysis on the tweet text using TextBlob, resulting in a polarity and subjectivity score. Both scores are added to a dictionary
along with the tweet text and coordinates and stored as a BSON document in MongoDB.