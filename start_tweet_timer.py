import logging
import os.path
import threading

import twitter
import yaml

import wakeup.util as util
from wakeup.twitter import send_tweet_after_delay
from wakeup.user_activity import execute_on_user_activity
from wakeup.constants import LOG_FILE_NAME, CONFIG_FILE_NAME


def main():
    configure_logging(logging.INFO)
    logging.info("Script started")
    config = load_config_file()
    send_tweet_if_user_overslept(config)


def configure_logging(level):
    user_home = util.get_user_home()
    log_file = os.path.join(user_home, LOG_FILE_NAME)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s",
        level=level,
        filename=log_file,
    )


def load_config_file():
    """Attempts to load the config file from the current user's
    home directory.

    Raises an exception if the file does not exist."""

    try:
        return try_load_config()
    except FileNotFoundError:
        logging.error("Config file does not exist")
        raise


def try_load_config():
    user_home = util.get_user_home()
    config_path = os.path.join(user_home, CONFIG_FILE_NAME)
    logging.info(f"Attempting to load config file from {config_path}")
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        logging.info("Successfully loaded config file")
        return config


def send_tweet_if_user_overslept(config):
    wait_for_tweet, cancel_tweet = send_tweet_after_delay(config)
    execute_on_user_activity(cancel_tweet)
    wait_for_tweet()


main()
