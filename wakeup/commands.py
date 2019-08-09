import os
import os.path
import subprocess

import yaml
from crontab import CronTab

import wakeup.config as config
import wakeup.util as util
from wakeup.schedule import Schedule, parse_schedule


def schedule(args):
    new_schedule = parse_schedule(" ".join([args.time, args.days_of_week]))
    cron = CronTab(user=True)
    cwd = os.getcwd()
    os.path.join(os.getcwd())
    which_result = subprocess.run(
        ["which", "pipenv"], capture_output=True, encoding="utf-8"
    )
    # On Linux, pynput uses the X window system to interact with the keyboard.
    # Therefore, the DISPLAY variable must be set, which is not the case when
    # this script is run as a cron job.
    pipenv_bin = which_result.stdout.strip()
    command = f"(cd '{os.getcwd()}' && env DISPLAY=':0' {pipenv_bin} run python start_tweet_timer.py)"
    job = cron.new(command=command)
    job.hour.on(new_schedule.hours)
    job.minutes.on(new_schedule.minutes)
    job.dow.on(*new_schedule.days_of_week)
    cron.write()


def status(args):
    cron = CronTab(user=True)
    job_descriptions = []
    for job in cron.find_command("start_tweet_timer.py"):
        desc = f"\t* {job.hours}:{job.minutes} on {job.dow}"
        job_descriptions.append(desc)

    if job_descriptions:
        first_line = "The following alarms are scheduled:"
        job_lines = "\n".join(job_descriptions)
        msg = "\n".join([first_line, job_lines])
    else:
        msg = "No alarms scheduled."

    print(msg)


def clear(args):
    cron = CronTab(user=True)
    num_jobs = cron.remove_all(command="start_tweet_timer.py")
    cron.write()

    print(f"Cleared {num_jobs} scheduled alarms.")


def init(args):
    skeleton_config = {
        config.CONSUMER_KEY: "<not set>",
        config.CONSUMER_SECRET: "<not set>",
        config.ACCESS_TOKEN_KEY: "<not set>",
        config.ACCESS_TOKEN_SECRET: "<not set>",
    }
    config.load_defaults(skeleton_config)

    user_home = util.get_user_home()
    config_path = os.path.join(user_home, "wakeup.yaml")
    with open(config_path, "w") as config_file:
        yaml.dump(skeleton_config, config_file)

    msg = f"""\
Created a config file at {config_path}. 
You still need to set all the Twitter API keys."""
    print(msg)
