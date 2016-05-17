from __future__ import absolute_import

import os
import sys
import argparse
import glob
import plistlib
import datetime
import pytz

from .app_config import AppConfig
from .package_config import PackageConfig, load_package_config
from .wrapper_config import WrapperConfig
from . import processor
from . import term
from . import util

APP_CONFIG_FILE_NAME = 'lnkr-import.toml'

EXIT_CODE_NO_CONFIG = 1
EXIT_CODE_DISALLOW_PACKAGE_CONFIG = 2
EXIT_CODE_DISALLOW_APP_CONFIG = 3
EXIT_CODE_INVALID_SECTION = 4

pwd = os.path.abspath('.')

def load_app_config(path):
    config = AppConfig(os.path.join(path, APP_CONFIG_FILE_NAME))
    if config.valid:
        return config
    else:
        return None

def load_config(allow_package, allow_app):
    config = load_package_config(pwd) or load_app_config(pwd)
    if config is None:
        term.error('Lnkr Config File Not Found: %s' % term.format_path(pwd))
        sys.exit(EXIT_CODE_NO_CONFIG)
    elif isinstance(config, PackageConfig):
        if allow_package:
            term.verbose('Packeg Config Loaded: %s' % term.format_path(config.path))
            return config
        else:
            sys.exit(EXIT_CODE_DISALLOW_PACKAGE_CONFIG)
    elif isinstance(config, AppConfig):
        if allow_app:
            term.verbose('App Config Loaded: %s' % term.format_path(config.path))
            return config
        else:
            sys.exit(EXIT_CODE_DISALLOW_APP_CONFIG)
    else:
        return None

def do_lint_package(package_config):
    term.info('Under Construction!')

def do_lint_app(app_config):
    term.info('Under Construction!')

def do_lint(args):
    config = load_config(True, True)
    if isinstance(config, PackageConfig):
        do_lint_package(config)
    elif isinstance(config, AppConfig):
        do_lint_app(config)

def do_clean(args):
    app_config = load_config(False, True)
    term.info('Under Construction!')

def do_diff(args):
    app_config = load_config(False, True)
    term.info('Under Construction!')

def do_link(args):
    app_config = load_config(False, True)
    processor.do_link_app(app_config)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Test Only, Do not do any real change')

    parser.add_argument('-l', '--lint', action='store_true',
                        help='Validate the lnkr config files')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Clean all links created by lnkr')
    parser.add_argument('-d', '--diff', action='store_true',
                        help='Show diffs between original files vs local files')

    args = parser.parse_args()
    term.set_verbose_mode(args.verbose)

    util.test_mode = args.test

    if args.lint:
        do_lint(args)
    elif args.clean:
        do_clean(args)
    elif args.diff:
        do_diff(args)
    else:
        do_link(args)
