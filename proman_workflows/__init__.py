# -*- coding: utf-8 -*-
# copyright: (c) 2021 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
'''Convenience tools to manage Git projects with Python.'''

import logging
import os
from typing import List

from invoke import Collection, Program

from proman_workflows import config, setup, exception
from proman_workflows.config import Config
# from proman_workflows.vcs import Git

from proman_workflows.git.hooks import hooks_tasks

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'proman-source'
__description__ = 'Convenience module to manage VCS tools with Python.'
__version__ = '0.1.0'
__license__ = 'MPL-2.0'
__copyright__ = 'Copyright 2021 Jesse Johnson.'


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


source_tree = get_source_tree()

# Assemble namespace for tasks
namespace = Collection()
namespace.add_collection(setup, name='setup')
namespace.add_collection(hooks_tasks, name='hooks')
# namespace.configure({'package': 'override-package'})
# print(namespace.task_names)

program = Program(
    version=__version__,
    namespace=namespace,
    name=__title__,
    binary='commit-workflow',
    binary_names=['commit-workflow'],
)

__all__ = [
    'program',
    'source_tree',
]
