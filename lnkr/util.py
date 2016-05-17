from __future__ import absolute_import

import os
import sys

from . import term

PACKAGE_CONFIG_FILE_NAME = 'lnkr-export.toml'
WRAPPER_CONFIG_FILE_NAME = 'lnkr-wrapper.toml'

ALL = 'all'
YES = 'yes'
NO = 'no'

test_mode = False

skip_change_confirm = False

def get_section_value(kind, values, key, optional):
    if not isinstance(values, dict):
        term.error('[%s] Section Should Be Dict: %s' % (kind, values))
    if key in values:
        return values[key]
    elif optional:
        return None
    else:
        term.error('[%s] Invalid Section: %s Not Exist -> %s' % (kind, key, values))
        sys.exit(EXIT_CODE_INVALID_SECTION)

def get_attribs(attribs_holders):
    attribs = {}
    for holder in attribs_holders:
        if not hasattr(holder, 'attribs'):
            continue
        for key in holder.attribs:
            value = holder.attribs[key]
            if key in attribs:
                old_value = attribs[key]
                if old_value != value:
                    info('Attrib Overrided: %s, %s -> %s' % (key, value, old_value))
            else:
                attribs[key] = value
    return attribs

def query_all_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"all": ALL, "a": ALL,
             "yes": YES, "y": YES,
             "no": NO, "n": NO}
    if default is None:
        prompt = " [a/y/n] "
    elif default == ALL:
        prompt = " [A/y/n] "
    elif default == YES:
        prompt = " [a/Y/n] "
    elif default == NO:
        prompt = " [a/y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        term.info('\n' + question + term.format_param(prompt))
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            term.info("Please respond with 'all' or 'yes' or 'no' "
                             "(or 'a' or 'y' or 'n').\n")

def confirm_change(question, default=None):
    global skip_change_confirm
    if skip_change_confirm:
        return True
    answer = query_all_yes_no(question, default)
    if answer == ALL:
        skip_change_confirm = True
        return True
    elif answer == YES:
        return True
    return False

