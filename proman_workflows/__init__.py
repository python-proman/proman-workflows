# -*- coding: utf-8 -*-
# copyright: (c) 2021 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Convenience tools to manage Git projects with Python.'''

import logging
import os
from typing import Any, List

from git import Repo
from invoke import Collection, Program

from proman_workflows import config, exception
from proman_workflows.config import Config
from proman_workflows.parser import CommitMessageParser
from proman_workflows.release import ReleaseController
from proman_workflows.vcs import GitFlow
from proman_workflows import conventional_commits

logging.getLogger(__name__).addHandler(logging.NullHandler())


__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'proman-source'
__description__ = 'Convenience module to manage VCS tools with Python.'
__version__ = '0.1.0'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2021 Jesse Johnson.'


def get_repo(path: str = os.getcwd()) -> Repo:
    '''Load the repository object.'''
    return Repo(os.path.join(path, '.git'), search_parent_directories=True)


def get_source_tree(
    basepath: str = os.getcwd(),
    filenames: List[str] = config.filenames
) -> Config:
    '''Get source tree from path.'''
    for filename in filenames:
        filepath = os.path.join(basepath, filename)
        if os.path.isfile(filepath):
            return Config(filepath=filepath)
    raise exception.PromanWorkflowException('no configuration found')


def get_release_controller(*args: Any, **kwargs: Any) -> ReleaseController:
    '''Create and return a release controller.'''
    basepath = kwargs.get('basepath', os.getcwd())
    filenames = kwargs.get('filenames', config.filenames)
    return ReleaseController(
        config=get_source_tree(basepath=basepath, filenames=filenames),
        workflow=GitFlow(get_repo(basepath))
    )


repo = get_repo()
source_tree = get_source_tree()
parser = CommitMessageParser()


# Assemble namespace for tasks
namespace = Collection()
namespace.add_collection(conventional_commits, name='commit_hook')
# namespace.configure({'package': 'override-package'})
# print(namespace.task_names)

program = Program(
    version=__version__,
    namespace=namespace,
    name=__title__,
    binary='conventional-commit',
    binary_names=['conventional-commit'],
)

__all__ = ['repo', 'source_config', 'parser']
