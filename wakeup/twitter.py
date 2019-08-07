import threading

from wakeup.config import is_valid, USER_ACTIVITY_TIMEOUT, TWEET_TEXT
from wakeup.errors import MissingConfigValueError


def send_tweet_after_delay(config):

    if not is_valid(config):
        raise MissingConfigValueError()

    delay_in_minutes = config[USER_ACTIVITY_TIMEOUT]
    delay_in_seconds = 60 * delay_in_minutes

    def dummy_send_tweet():
        print(f'Mock sending tweet: {config[TWEET_TEXT]}')

    tweet_timer = threading.Timer(delay_in_seconds, dummy_send_tweet)
    tweet_timer.start()

    def cancel():
        tweet_timer.cancel()
    def wait():
        tweet_timer.join()

    return wait, cancel
