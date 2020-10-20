# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

import re
from git import Repo

from ..message import MessageParser

repo = Repo('.')


def search(sha: str = None):
    pass


def validate(sha: str = None):
    if hash:
        rex = re.compile('^[a-fA-F0-9]{40}$')
        branch = rex.match(str(sha))
        print(repo.tree(branch.group()))
    commit = repo.head.commit
    message_parser = MessageParser()
    message_parser.parse(commit.message)
