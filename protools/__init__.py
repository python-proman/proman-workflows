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

from protools import (
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
from protools.collection import Collection
from protools.config import DocsConfig

# from protools.vcs import Git

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'protoolss'
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


dirs = AppDirs(project_name='protoolss')
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

protools_namespace = Collection().from_module(init)
protools_namespace.configure(
    {
        'dirs': asdict(dirs),
        'spec': specfile.data,
        'python_path': config.python_path,
        'repo_dir': config.repo_dir,
        'working_dir': config.working_dir,
        'templates_dir': config.templates_dir,
    }
)
protools_namespace.load_collections(
    collections=[
        {
            'name': 'vcs',
            'driver_name': 'git',
            'driver_namespace': 'protools.vcs',
        },
        {
            'name': 'sort-headers',
            'driver_name': 'isort',
            'driver_namespace': 'protools.formatter',
        },
        {
            'name': 'format',
            'driver_name': 'black',
            'driver_namespace': 'protools.formatter',
        },
        {
            'name': 'gpg',
            'driver_name': 'gpg',
            'driver_namespace': 'protools.pki',
        },
        {
            'name': 'tls',
            'driver_name': 'tls',
            'driver_namespace': 'protools.pki',
        },
    ]
)
protools_namespace.add_collection(git.namespace, name='vcs')
protools = Program(
    version=__version__,
    namespace=protools_namespace,
    name=__title__,
    binary='project',
    binary_names=['project'],
)

__all__ = [
    'protools',
    'workflow',
]
