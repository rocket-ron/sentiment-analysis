from termcolor import colored


class ConsoleTweetSerializer:
    def __init__(self):
        pass

    @staticmethod
    def write(tweet):
        try:
            print '@%s: %s' % (
                colored(tweet['user']['screen_name'], 'yellow'),
                colored(tweet['text'].encode('ascii', 'ignore'), 'green'))
        except:
            pass

    def end(self):
        pass


if __name__ == '__main__':
    s = ConsoleTweetSerializer()
    u = {'screen_name': 'joe blow'}
    t = {'user': u, 'text': 'this is a test. This is only a test...'}
    s.write(t)
