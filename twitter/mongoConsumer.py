#!/usr/bin/python

import argparse
import json
from kafka import KafkaConsumer
from pymongo import MongoClient


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
                    require=False,
                    help='The port of the Kafka broker if using Kafka serialization')
parser.add_argument('--mongohost',
                    type=str,
                    require=False,
                    help='The host name of the mongoDB server')
parser.add_argument('--mongoport',
                    type=str,
                    require=False,
                    help='The port number of the mongoDB server')

args = parser.parse_args()

mongo_client = MongoClient(host=args.mongohost, port=args.mongoport)

kafka_server = "{0}:{1}".format(args.kafkahost, args.kafkaport)

consumer = KafkaConsumer('tweets',
                         group_id='tweet-group',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         bootstrap_servers=[kafka_server])

for message in consumer:
    mongo_client.tweets.tweets.save(message)





