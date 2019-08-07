CONSUMER_KEY = 'consumer_key'
CONSUMER_SECRET = 'consumer_secret'
ACCESS_TOKEN_KEY = 'access_token_key'
ACCESS_TOKEN_SECRET = 'access_token_secret'
USER_ACTIVITY_TIMEOUT = 'user_activity_timeout'
TWEET_TEXT = 'tweet'

def load_defaults(config):
    """Populate config with defaults for missing optional values."""

    if USER_ACTIVITY_TIMEOUT not in config:
        config[USER_ACTIVITY_TIMEOUT] = 60
    if TWEET_TEXT not in config:
        config[TWEET_TEXT] = """I should be working, \
but I'm sleeping in instead..."""

def is_valid(config):
    return (CONSUMER_KEY in config
        and CONSUMER_SECRET in config
        and ACCESS_TOKEN_KEY in config
        and ACCESS_TOKEN_SECRET in config)
