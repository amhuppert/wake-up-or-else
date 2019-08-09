import os
import os.path
import subprocess

import yaml
from crontab import CronTab

import wakeup.config as config
import wakeup.util as util
from wakeup.schedule import Schedule, parse_schedule
from wakeup.constants import CONFIG_FILE_NAME, ALARM_SCRIPT_NAME


def schedule(args):
    alarm_schedule = parse_schedule(" ".join([args.time, args.days_of_week]))
    _add_cron_job(alarm_schedule)


def _add_cron_job(schedule: Schedule):
    cron = CronTab(user=True)
    command = _create_cron_command()
    job = cron.new(command=command)
    _set_job_time(job, schedule)
    cron.write()


def _create_cron_command():
    pipenv_bin = _find_pipenv_bin()
    # On Linux, pynput uses the X window system to interact with the keyboard.
    # Therefore, the DISPLAY variable must be set, which is not the case when
    # this script is run as a cron job.
    command = f"(cd '{os.getcwd()}' && env DISPLAY=':0' {pipenv_bin} run python {ALARM_SCRIPT_NAME})"
    return command


def _find_pipenv_bin():
    which_result = subprocess.run(
        ["which", "pipenv"], capture_output=True, encoding="utf-8"
    )
    return which_result.stdout.strip()


def _set_job_time(job, schedule: Schedule):
    job.hour.on(schedule.hours)
    job.minutes.on(schedule.minutes)
    job.dow.on(*schedule.days_of_week)


def status(args):
    cron = CronTab(user=True)
    job_descriptions = []
    for job in cron.find_command(ALARM_SCRIPT_NAME):
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
    num_jobs = cron.remove_all(command=ALARM_SCRIPT_NAME)
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
    config_path = os.path.join(user_home, CONFIG_FILE_NAME)
    with open(config_path, "w") as config_file:
        yaml.dump(skeleton_config, config_file)

    msg = f"""\
Created a config file at {config_path}. 
You still need to set all the Twitter API keys."""
    print(msg)
