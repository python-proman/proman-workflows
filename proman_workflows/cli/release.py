# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

import logging
import re
from typing import Optional

from proman_workflows import repo, source_config
from proman_workflows.parser import CommitMessageParser
from proman_workflows.releases import CommitMessageAction

log = logging.getLogger(__name__)

workflow = CommitMessageAction(
    name='test',
    config=source_config,
)

# def search(digest: str):
#     pass


def version(name: str = 'master') -> None:
    ref = repo.refs[name].commit
    workflow.parse(ref.message)
    title = workflow.title
    if title['type'] == 'feat':
        print('this is a minor bump')
    if title['type'] == 'fix':
        print('this is a patch')
    # 'build'
    # 'chore'  # deprecated (see: build and ci)
    # 'ci'
    # 'docs'
    # 'style'
    # 'refactor'
    # 'perf'
    # 'test'
    print(workflow.current_version)
    # workflow.version()


def validate(digest: Optional[str] = None) -> None:
    if digest:
        rex = re.compile('^[a-fA-F0-9]{40}$')
        branch = rex.match(str(digest))
        print(repo.tree(branch.group()) if branch else None)
    commit = repo.head.commit
    parser = CommitMessageParser()
    parser.parse(commit.message)
    print(parser.title)
