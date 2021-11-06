# copyright: (c) 2021 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
"""Provide convenience tool to manage projects with Python."""

import logging
import os
from dataclasses import asdict
from typing import List

from invoke import Program
from proman_common.config import Config
from proman_common.filepaths import AppDirs

from proman_workflows import (
    config,
    container,
    docs,
    exception,
    git,
    init,
    package,
    qa,
    security,
    utils,
)
from proman_workflows.collection import Collection
from proman_workflows.config import DocsConfig

# from proman_workflows.vcs import Git

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'proman-workflows'
__description__ = 'Convenience module to manage project tools with Python.'
__version__ = '0.1.0'
__license__ = 'MPL-2.0'
__copyright__ = 'Copyright 2021 Jesse Johnson.'

logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_specfile(
    project_dir: str = config.project_dir,
    specfiles: List[str] = config.specfiles,
) -> Config:
    """Get source tree from path."""
    for specfile in specfiles:
        filepath = os.path.join(project_dir, specfile)
        if os.path.isfile(filepath):
            return Config(filepath=filepath)
    raise exception.PromanWorkflowException('no configuration found')


dirs = AppDirs(project_name='proman-workflows')
specfile = get_specfile()
docs_config = DocsConfig()

workflow_namespace = Collection()
workflow_namespace.configure(
    {
        'dirs': asdict(dirs),
        'spec': specfile.data,
        'docs': asdict(docs_config),
        'working_dir': config.working_dir,
        'container_runtime': config.container_runtime,
    }
)
workflow_namespace.add_collection(container.namespace, name='container')
workflow_namespace.add_collection(docs.namespace, name='docs')
workflow_namespace.add_collection(package.namespace, name='dist')
workflow_namespace.add_collection(qa.namespace, name='qa')
workflow_namespace.add_collection(security.namespace, name='sec')
workflow_namespace.add_collection(utils.tasks, name='utils')
workflow = Program(
    version=__version__,
    namespace=workflow_namespace,
    name=__title__,
    binary='workflow',
    binary_names=['workflow'],
)

project_namespace = Collection().from_module(init)
project_namespace.configure(
    {
        'dirs': asdict(dirs),
        'spec': specfile.data,
        'python_path': config.python_path,
        'repo_dir': config.repo_dir,
        'working_dir': config.working_dir,
        'templates_dir': config.templates_dir,
    }
)
project_namespace.load_collections(
    collections=[
        {
            'name': 'vcs',
            'driver_name': 'git',
            'driver_namespace': 'proman.workflow.vcs',
        },
        {
            'name': 'sort-headers',
            'driver_name': 'isort',
            'driver_namespace': 'proman.workflow.formatter',
        },
        {
            'name': 'format',
            'driver_name': 'black',
            'driver_namespace': 'proman.workflow.formatter',
        },
        {
            'name': 'gpg',
            'driver_name': 'gpg',
            'driver_namespace': 'proman.workflow.pki',
        },
        {
            'name': 'tls',
            'driver_name': 'tls',
            'driver_namespace': 'proman.workflow.pki',
        },
    ]
)
project_namespace.add_collection(git.namespace, name='vcs')
project = Program(
    version=__version__,
    namespace=project_namespace,
    name=__title__,
    binary='project',
    binary_names=['project'],
)

__all__ = [
    'project',
    'workflow',
]
