# -*- coding: utf-8 -*-
# copyright: (c) 2021 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
'''Convenience tools to manage projects with Python.'''

import logging
import os
from typing import List

from invoke import Collection, Program
from proman_common.config import Config

from proman_workflows import package, config, setup, exception

# from proman_workflows.vcs import Git
from proman_workflows.pki import gpg
from proman_workflows.git.hooks import hooks_tasks

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'proman-workflows'
__description__ = 'Convenience module to manage project tools with Python.'
__version__ = '0.1.0'
__license__ = 'MPL-2.0'
__copyright__ = 'Copyright 2021 Jesse Johnson.'


def get_specfile(
    basepath: str = os.getcwd(),
    filenames: List[str] = config.filenames,
) -> Config:
    '''Get source tree from path.'''
    for filename in filenames:
        filepath = os.path.join(basepath, filename)
        if os.path.isfile(filepath):
            return Config(filepath=filepath)
    raise exception.PromanWorkflowException('no configuration found')


specfile = get_specfile()

# Assemble namespace for tasks
workflow_namespace = Collection()
workflow_namespace.add_collection(package)
workflow_namespace.add_collection(setup, name='setup')
workflow_namespace.add_collection(hooks_tasks, name='hooks')
workflow_namespace.configure(
    {
        'python_path': config.python_path,
        'spec': specfile.data,
    }
)
# print(workflow_namespace.task_names)

workflow = Program(
    version=__version__,
    namespace=workflow_namespace,
    name=__title__,
    binary='workflow',
    binary_names=['workflow'],
)

pki_namespace = Collection()
pki_namespace.add_collection(Collection.from_module(gpg))
pki_namespace.configure({'spec': specfile.data})

pki = Program(
    version=__version__,
    namespace=pki_namespace,
    name=__title__,
    binary='pki',
    binary_names=['pki'],
)

__all__ = [
    'pki',
    'workflow',
]
