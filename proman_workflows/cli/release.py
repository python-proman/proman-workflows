# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

import logging
import re
from typing import Optional

from proman_workflows import repo, parser, get_release_controller

log = logging.getLogger(__name__)

workflow = get_release_controller()


# def search(digest: str) -> None:
#     pass


def version(
    bump: bool = False,
    # branch: str = 'master'
) -> None:
    if bump:
        workflow.bump_version()
    print(workflow.version)


def validate(digest: Optional[str] = None) -> None:
    if digest:
        rex = re.compile('^[a-fA-F0-9]{40}$')
        branch = rex.match(str(digest))
        print(repo.tree(branch.group()) if branch else None)
    commit = repo.head.commit
    parser.parse(commit.message)
    print(parser.title)
