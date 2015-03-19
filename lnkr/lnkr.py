import os
import sys
import argparse
import glob
import plistlib
import datetime
import pytz
from blessings import Terminal

term = Terminal()

test_mode = False
verbose_mode = False
clean_mode = False


def info(msg):
    print term.normal + msg


def verbose(msg):
    if verbose_mode:
        info(msg)


def error(msg):
    print term.red + msg


def format_error(err):
    return term.red(err)


def format_path(path):
    return term.blue(path)


def format_param(param):
    return term.yellow(param)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Test Only, Do not do any real change')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Clean, Remove links created by lnkr')

    args = parser.parse_args()
    global test_mode
    test_mode = args.test
    global verbose_mode
    verbose_mode = args.verbose
    global clean_mode
    clean_mode = args.clean

    info('Under Construction!')
