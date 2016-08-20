from tweepy.streaming import StreamListener
from tweepy import Stream
import twitterAuth
import json
import time
import signal
import threading


class TwitterStreamListener(StreamListener):

    def __init__(self, serializer, key):
        signal.signal(signal.SIGINT, self.interrupt)
        self._lock = threading.RLock()

        self.serializer = serializer
        self.auth = twitterAuth.get_oauth(key)
        self.retryCount = 0
        self.retryTime  = 1
        self.retryMax	= 5
        self.caughtInterrupt = False
        self.twitterStream = None
        self.geo_only = False

    def on_data(self, data):
        # process data
        with self._lock:
            if not self.caughtInterrupt:
                tweet = json.loads(data)
                if self.geo_only and 'coordinates' in tweet:
                    self.serializer.write(tweet)
                return True
            else:
                self.serializer.end()
                return False

    def on_error(self, status_code):
        if status_code == 420:
            self.retryCount += 1
            if self.retryCount > self.retryMax:
                return False
            else:
                time.wait(self.retryTime)
                self.retryTime *= 2
                return True

    def interrupt(self, signum, frame):
        print "CTRL-C caught, closing..."
        with self._lock:
            self.caughtInterrupt = True

    def track(self, track):
        self.twitterStream = Stream(self.auth, self)
        self.twitterStream.filter(track=[track])

    def sample(self, geo_only=False):
        self.geo_only = geo_only
        self.twitterStream = Stream(self.auth, self)
        self.twitterStream.sample(async=False)

    def locate(self, locations):
        self.geo_only = True
        self.twitterStream = Stream(self.auth, self)
        self.twitterStream.filter(locations=locations)
