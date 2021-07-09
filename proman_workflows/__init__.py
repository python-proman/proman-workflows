# -*- coding: utf-8 -*-
# copyright: (c) 2021 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Convenience tools to manage Git projects with Python.'''

import logging
import os
from typing import Any, List, Union

from git import Repo
from invoke import Collection, Program

from proman_workflows import config, setup, exception
from proman_workflows.config import Config
from proman_workflows.controller import IntegrationController
from proman_workflows.grammars.conventional_commits import CommitMessageParser
from proman_workflows.vcs import Git
from proman_workflows.version import PythonVersion

from proman_workflows.git.hooks import hooks_tasks

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
    return Git(os.path.join(path))


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


def get_python_version(cfg: Union[Config, str]) -> PythonVersion:
    if isinstance(cfg, Config):
        if cfg.retrieve('/tool/proman'):
            if 'version' in cfg['tool']['proman']['release']:
                version = cfg.retrieve('/tool/proman/release/version')
            else:
                version = cfg.retrieve('/tool/proman/version')
        elif cfg.retrieve('/tool/poetry'):
            version = cfg.retrieve('/tool/poetry/version')
        elif cfg.retrieve('/metadata'):
            version = cfg.retrieve('/metadata/version')
        else:
            raise exception.PromanWorkflowException('no version found')
    else:
        version = cfg
    return PythonVersion(version)


def get_release_controller(*args: Any, **kwargs: Any) -> IntegrationController:
    '''Create and return a release controller.'''
    basepath = kwargs.get('basepath', os.getcwd())
    filenames = kwargs.get('filenames', config.filenames)
    cfg = get_source_tree(basepath=basepath, filenames=filenames)
    version = get_python_version(kwargs.pop('version', cfg))
    return IntegrationController(
        version=version,
        config=cfg,
        repo=get_repo(basepath),
        **kwargs,
    )


repo = get_repo()
source_tree = get_source_tree()
parser = CommitMessageParser()

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
    'get_repo',
    'get_source_tree',
    'get_release_controller',
    'parser',
    'repo',
    'source_tree',
]
