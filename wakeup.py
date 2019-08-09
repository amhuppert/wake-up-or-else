"""Command line interface to the script"""

import wakeup.argparse

args = wakeup.argparse.parse_args()
args.run_command(args)
