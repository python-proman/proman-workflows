# copyright: (c) 2021 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
"""Provide convenience tool to manage projects with Python."""

import logging
from dataclasses import asdict

from proman_workflows import WorkflowProgram, __title__, __version__, config
from proman_workflows.collection import Collection
from proman_workflows.config import DocsConfig, WorkflowConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())

project_config = config.ProjectConfig(
    docs=asdict(DocsConfig()),
    plugins=[
        config.Plugin(
            name='vcs',
            driver_name='git',
            driver_namespace='proman.workflows.vcs',
        ),
        config.Plugin(
            name='sort-headers',
            driver_name='isort',
            driver_namespace='proman.workflows.formatter',
        ),
        config.Plugin(
            name='format',
            driver_name='black',
            driver_namespace='proman.workflows.formatter',
        ),
        config.Plugin(
            name='gpg',
            driver_name='gpg',
            driver_namespace='proman.workflows.pki',
        ),
        config.Plugin(
            name='tls',
            driver_name='tls',
            driver_namespace='proman.workflows.pki',
        ),
    ],
)
namespace = Collection()
namespace.configure(asdict(project_config))
namespace.load_collections()

tools = WorkflowProgram(
    name=__title__,
    namespace=namespace,
    binary='tools',
    binary_names=['tools'],
    config_class=WorkflowConfig,
    version=__version__,
)

__all__ = ['namespace', 'tools']
