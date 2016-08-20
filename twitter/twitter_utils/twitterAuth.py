import tweepy
import os


def get_app_auth(app):
    keys = get_auth_keys(app)
    if len(keys) < 4:
        print "Error retrieving Twitter keys for authorization..."
        return None
    else:
        return tweepy.AppAuthHandler(keys['app_key'], keys['app_secret'])


def get_oauth(app):
    keys = get_auth_keys(app)
    auth = tweepy.OAuthHandler(keys['app_key'], keys['app_secret'])
    auth.set_access_token(keys['access_token'], keys['token_secret'])
    return auth


# keys are environment variables with the patterns
# TWITTER_[app]_APP_KEY
# TWITTER_[app]_CONSUMER_SECRET
# etc
def get_auth_keys(app):
    if app:
        app += '_'
    else:
        app = ''

    keys = dict(app_key=os.getenv('TWITTER_' + app + 'APP_KEY'),
                app_secret=os.getenv('TWITTER_' + app + 'CONSUMER_SECRET'),
                access_token=os.getenv('TWITTER_' + app + 'ACCESS_TOKEN'),
                token_secret=os.getenv('TWITTER_' + app + 'ACCESS_TOKEN_SECRET'))
    return keys
