import threading
import logging

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
        logging.error("Missing required config value. Aborting..")
        raise MissingConfigValueError()

    delay_in_minutes = config[USER_ACTIVITY_TIMEOUT]
    delay_in_seconds = 60 * delay_in_minutes

    logging.info(
        f"Will listen for user activity for the next {delay_in_minutes} minutes"
    )

    def send_tweet():
        logging.info("Time has expired. Proceeding to post tweet.")
        twitter_api = twitter.Api(
            consumer_key=config[CONSUMER_KEY],
            consumer_secret=config[CONSUMER_SECRET],
            access_token_key=config[ACCESS_TOKEN_KEY],
            access_token_secret=config[ACCESS_TOKEN_SECRET],
        )
        logging.info(f"Attempting to post tweet: '{config[TWEET_TEXT]}'...")
        twitter_api.PostUpdate(config[TWEET_TEXT])
        logging.info("Success! Tweet posted.")

    tweet_timer = threading.Timer(delay_in_seconds, send_tweet)
    tweet_timer.start()

    def cancel():
        logging.info("Tweet cancelled..")
        tweet_timer.cancel()

    def wait():
        tweet_timer.join()

    return wait, cancel
