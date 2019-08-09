# Wake Up or Else
Create extra incentive to get up early by alerting all of your Twitter followers when you don't.

If you're not actively working on your computer soon after your alarm goes off, 
this script will tweet something from your account. 
The scheduled tweet is will be cancelled automatically as soon as any mouse 
or keyboard activity is detected within a configurable window of time.

## Requirements
- Linux system
- cron
- [pipenv](https://docs.pipenv.org)
- a [Twitter developer account](https://developer.twitter.com)

## How to use

This project uses pipenv for dependency management. 
For best results, use pipenv to install all dependencies inside a virtual environment.

1. Create an app in Twitter and generate some API keys and tokens.
2. Create a config file: `python wakeup.py init`
3. Add Twitter API keys to config file.
4. Schedule an alarm: `python wakeup.py schedule 5:30am mon,tue,wed,thu,fri`
5. For help, run `python wakeup.py --help`

## Configuration

The config file is located at `$HOME/wakeup.yaml`.
Besides the Twitter API keys and tokens, 
you can configure the amount of time to wait for user activity 
and the content of the tweet.


### `tweet`
Set the `tweet` property to whatever you want to tweet out if you decide to sleep in
&mdash; ideally something that's mildly embarrassing but that won't get you fired.

### `user_activity_timeout`
The `user_activity_timeout` property is the number of **minutes** 
the script will wait for user activity after the alarm time.

So if you schedule an alarm for 6:30AM and set `user_activity_timeout` to 60, the script will
monitor for mouse and keyboard activity between 6:30AM to 7:30AM. 
The tweet will be sent out at 7:30AM if no activity is detected. 
