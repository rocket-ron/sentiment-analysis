#!/usr/bin/python

from twitter_utils.apikeys import apikeys
from twitter_utils.twitterStreamListener import TwitterStreamListener
from tweet_serializers.consoleTweetSerializer import ConsoleTweetSerializer
from tweet_serializers.kafkaTweetSerializer import KafkaTweetSerializer
import argparse
import time


parser = argparse.ArgumentParser(
    description='Attach to the twitter stream API and send the tweets to a destination',
    add_help=True,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--key',
                    type=str,
                    required=True,
                    choices=apikeys.keys(),
                    help='the Twitter API key to use')
parser.add_argument('--track',
                    type=str,
                    required=False,
                    help='Twitter phrases to track')
parser.add_argument('--locations',
                    action='store_true',
                    required=False,
                    help='Filter the Twitter stream for geo-located tweets')
parser.add_argument('--sample',
                    action='store_true',
                    required=False,
                    help='Sample the Twitter stream')
parser.add_argument('--serializer',
                    choices=['console', 'kafka'],
                    help='Where to send the tweets.'
                    )
parser.add_argument('--kafkahost',
                    type=str,
                    required=False,
                    help='The host name of the Kafka broker if using Kafka serialization')
parser.add_argument('--kafkaport',
                    type=int,
                    required=False,
                    help='The port of the Kafka broker if using Kafka serialization')

args = parser.parse_args()

if args.serializer == 'console':
    print "Writing tweets to console..."
    serializer = ConsoleTweetSerializer()
    fetchSize = 10
else:
    print "Writing tweets to Kafka..."
    serializer = KafkaTweetSerializer(host=args.kafkahost, port=args.kafkaport)

startTime = time.time()

listener = TwitterStreamListener(serializer, apikeys[args.key])

if args.sample:
    listener.sample()
elif args.locations:
    try:
        listener.locate(locations=[-180, -90, 180, 90])
    except KeyboardInterrupt:
        listener.disconnect()
else:
    if args.track is not None:
        listener.track(args.track)

print "Tracking stopped after " + str(time.time() - startTime) + " seconds."
