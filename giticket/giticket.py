# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import io
import re
import subprocess
import sys

import six

underscore_split_mode = 'underscore_split'
regex_match_mode = 'regex_match'


def update_commit_message(filename, regex):
    with io.open(filename, 'r+') as fd:
        contents = fd.readlines()
        commit_msg = contents[0]
        # Check if we can grab ticket info from branch name.
        branch = get_branch_name()

        # Bail if commit message already contains tickets
        if re.search(regex, commit_msg):
            return

        tickets = re.findall(regex, branch)
        if tickets:
            new_commit_msg = f"[{tickets[0]}] {commit_msg}"

            contents[0] = six.text_type(new_commit_msg)
            fd.seek(0)
            fd.writelines(contents)
            fd.truncate()


def get_branch_name():
    # Only git support for right now.
    return subprocess.check_output(
        [
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD',
        ],
    ).decode('UTF-8')


def main(argv=None):
    """This hook saves developers time by prepending ticket numbers to commit-msgs.
    For this to work the following two conditions must be met:

        - The ticket format regex specified must match.
        - The branch name format must be <ticket number>_<rest of the branch name>
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args(argv)
    regex = r"HYPER-[0-9]+" # noqa
    update_commit_message(args.filenames[0], regex)


if __name__ == '__main__':
    sys.exit(main())
