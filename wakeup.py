import threading
import twitter
import yaml
from wakeup.user_activity import execute_on_user_activity
from wakeup.twitter import send_tweet_after_delay

def main():
    config = load_config()
    send_tweet_if_user_overslept(config)

def load_config():
    """Attempts to load the wakeup.yaml file from the current user's
    home directory.

    Raises an exception if the file does not exist."""

    try:
        return do_load_config()
    except FileNotFoundError:
        print("Config file does not exist")
        raise

def do_load_config():
    # TODO replace hardcoded path
    with open('/home/alex/wakeup.yaml', 'r') as config_file:
        config = yaml.load(config_file)
        # TODO Better mechanism for logging?
        print(f'Config file loaded: {config}')
        return config

def send_tweet_if_user_overslept(config):
    wait_for_tweet, cancel_tweet = send_tweet_after_delay(config)
    execute_on_user_activity(cancel_tweet)
    wait_for_tweet()

main()