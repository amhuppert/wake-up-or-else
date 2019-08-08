import threading

import twitter

from wakeup.config import (
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET,
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TWEET_TEXT,
    USER_ACTIVITY_TIMEOUT,
    is_valid,
)
from wakeup.errors import MissingConfigValueError


def send_tweet_after_delay(config):

    if not is_valid(config):
        raise MissingConfigValueError()

    delay_in_minutes = config[USER_ACTIVITY_TIMEOUT]
    delay_in_seconds = 60 * delay_in_minutes

    def send_tweet():
        twitter_api = twitter.Api(
            consumer_key=config[CONSUMER_KEY],
            consumer_secret=config[CONSUMER_SECRET],
            access_token_key=config[ACCESS_TOKEN_KEY],
            access_token_secret=config[ACCESS_TOKEN_SECRET],
        )
        print(f"Posting tweet: '{config[TWEET_TEXT]}'...")
        twitter_api.PostUpdate(config[TWEET_TEXT])
        print("Tweet posted.")

    tweet_timer = threading.Timer(delay_in_seconds, send_tweet)
    tweet_timer.start()

    def cancel():
        tweet_timer.cancel()

    def wait():
        tweet_timer.join()

    return wait, cancel
