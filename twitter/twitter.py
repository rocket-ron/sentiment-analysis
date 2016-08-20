#!/usr/bin/python

from twitter_utils.apikeys import apikeys
from twitter_utils.twitterStreamListener import TwitterStreamListener
from tweet_serializers.consoleTweetSerializer import ConsoleTweetSerializer
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

args = parser.parse_args()


# fetchSize = 1500

print "Writing tweets to console..."
serializer = ConsoleTweetSerializer()
fetchSize = 10

startTime = time.time()

listener = TwitterStreamListener(serializer, apikeys[args.key])

if args.sample:
    listener.sample()
elif args.locations:
    listener.locate(locations=[-180, -90, 180, 90])
else:
    if args.track is not None:
        listener.track(args.track)

print "Tracking stopped after " + str(time.time() - startTime) + " seconds."
