# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

import re
from typing import Optional

from git import Repo

from proman_workflows.parser import CommitMessageParser

repo = Repo('.')


def search(digest: str):
    pass


def validate(digest: Optional[str] = None):
    if hash:
        rex = re.compile('^[a-fA-F0-9]{40}$')
        branch = rex.match(str(digest))
        print(repo.tree(branch.group()))
    commit = repo.head.commit
    message_parser = CommitMessageParser()
    message_parser.parse(commit.message)
