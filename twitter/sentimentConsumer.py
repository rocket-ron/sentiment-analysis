#!/usr/bin/python

import argparse
import json
from kafka import KafkaConsumer
from redis import Redis
from rq import Queue
from sentiments.sentimentProcessor import process_tweet

parser = argparse.ArgumentParser(
    description='Attach to the twitter stream API and send the tweets to a destination',
    add_help=True,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--kafkahost',
                    type=str,
                    required=False,
                    help='The host name of the Kafka broker if using Kafka serialization')
parser.add_argument('--kafkaport',
                    type=int,
                    required=False,
                    help='The port of the Kafka broker if using Kafka serialization')
parser.add_argument('--mongohost',
                    type=str,
                    required=False,
                    help='The host name of the mongoDB server')
parser.add_argument('--mongoport',
                    type=int,
                    required=False,
                    help='The port number of the mongoDB server')
parser.add_argument('--redishost',
                    type=str,
                    required=False,
                    help='The host name of the Redis cache')
parser.add_argument('--redisport',
                    type=int,
                    required=False,
                    help='The port of the Redis Cache')

args = parser.parse_args()


kafka_server = "{0}:{1}".format(args.kafkahost, args.kafkaport)

redis_conn = Redis(host=args.redishost, port=args.redisport)
q = Queue(connection=redis_conn)

consumer = KafkaConsumer('tweets',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         bootstrap_servers=[kafka_server])

for message in consumer:
    try:
        job = q.enqueue(process_tweet, args=(message, args.mongohost, args.mongoport, 'tweets'))

    except KeyboardInterrupt:
        consumer.close()
