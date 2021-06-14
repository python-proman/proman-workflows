# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

import logging
import re
from typing import Optional

from proman_workflows import repo, source_config
from proman_workflows.parser import CommitMessageParser
from proman_workflows.releases import GitFlow

log = logging.getLogger(__name__)

workflow = GitFlow(
    name='test',
    config=source_config,
)

# def search(digest: str):
#     pass


def version() -> None:
    ref = repo.refs['origin/master']
    print(ref)
    workflow.parse(ref)
    print(workflow.current_version)
    workflow.version()


def validate(digest: Optional[str] = None) -> None:
    if digest:
        rex = re.compile('^[a-fA-F0-9]{40}$')
        branch = rex.match(str(digest))
        print(repo.tree(branch.group()) if branch else None)
    commit = repo.head.commit
    commit_message = CommitMessageParser()
    commit_message.parse(commit.message)
    print(commit_message.title)
