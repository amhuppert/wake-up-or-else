import argparse
import wakeup.schedule as schedule
import wakeup.commands as commands

description = """\
This program is designed to give you a little extra motivation to get out of \
bed when your alarm clock goes off. You can schedule an embarrassing tweet \
to be sent if you're not actively working on your computer by a certain time. \

The tweet will automatically be cancelled if any mouse or keyboard activity \
is detected within a configurable window from the time your alarm goes off."""


parser = argparse.ArgumentParser(description=description)
subparsers = parser.add_subparsers(dest="command", required=True)

schedule_help = "Set up %(prog)s to run when your alram goes off"
schedule_command = subparsers.add_parser("schedule", help=schedule_help)
schedule_command.add_argument(
    "time", help="The time the script should run. (Ex: '6:30am', '1:30pm', '13:30')"
)
schedule_command.add_argument(
    "days_of_week",
    help="""Days on which the script should run. \
Choose any combination of {mon,tue,wed,thu,fri,sat,sun}, \
separated by commas (no spaces). Defaults to every day of the week""",
    default=",".join(schedule.get_all_weekdays()),
    nargs="?",
)
schedule_command.set_defaults(run_command=commands.schedule)

status_command = subparsers.add_parser("status", help="Show any scheduled periods")
status_command.set_defaults(run_command=commands.status)

clear_command = subparsers.add_parser("clear", help="Remove all scheduled periods")
clear_command.set_defaults(run_command=commands.clear)

init_help = """\
Create a config file at $HOME/wakeup.yaml. \
You must add all Twitter API keys to the config file in order for \
this script to be functional."""
init_command = subparsers.add_parser("init", help=init_help)
init_command.set_defaults(run_command=commands.init)


def parse_args():
    return parser.parse_args()
