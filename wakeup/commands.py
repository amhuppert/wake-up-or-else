from wakeup.schedule import parse_schedule, Schedule
from crontab import CronTab
import os
import os.path
import subprocess


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
    #     os.environ["DISPLAY"] = ":0"
    pipenv_bin = which_result.stdout.strip()
    command = f"(cd '{os.getcwd()}' && env DISPLAY=':0' {pipenv_bin} run python start_tweet_timer.py)"
    job = cron.new(command=command)
    job.hour.on(new_schedule.hours)
    job.minutes.on(new_schedule.minutes)
    job.dow.on(*new_schedule.days_of_week)
    cron.write()


def status(args):
    pass


def clear(args):
    pass


def init(args):
    pass
