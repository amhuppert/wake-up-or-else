import threading
import twitter
import yaml
from wakeup.user_activity import execute_on_user_activity
from wakeup.twitter import send_tweet_after_delay
import os.path


def main():
    config = load_config()
    send_tweet_if_user_overslept(config)


def load_config():
    """Attempts to load the wakeup.yaml file from the current user's
    home directory.

    Raises an exception if the file does not exist."""

    try:
        return try_load_config()
    except FileNotFoundError:
        print("Config file does not exist")
        raise


def try_load_config():
    user_home = os.path.expanduser("~")
    config_path = os.path.join(user_home, "wakeup.yaml")
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        return config


def send_tweet_if_user_overslept(config):
    wait_for_tweet, cancel_tweet = send_tweet_after_delay(config)
    execute_on_user_activity(cancel_tweet)
    wait_for_tweet()


main()
