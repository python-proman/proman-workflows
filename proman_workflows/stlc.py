# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Implement software testing life-cycle."""

import logging
# import os
# import shutil
# from dataclasses import asdict
from typing import TYPE_CHECKING

from invoke import Executor, task

# TODO: switch to executor
from proman_workflows import (
    # container,
    # docs,
    # init,
    # exception,
    package,
    qa,
    sca,
    # stlc,
    # utils,
)
from proman_workflows.collection import Collection
from proman_workflows.config import WorkflowConfig

if TYPE_CHECKING:
    from invoke import Context

logging.getLogger(__name__).addHandler(logging.NullHandler())


@task
def static_analysis(ctx):  # type: (Context) -> None
    """Perform static code analysis."""
    from pprint import pprint
    if 'plugins' in ctx:
        pprint(ctx.plugins)
    else:
        pprint(ctx.config.__dict__)
    print(sca.namespace.task_names)
    # Executor(
    #     sca.namespace,
    #     config=WorkflowConfig(ctx.config)
    # ).execute('package.publish')


@task
def install(ctx):  # type: (Context) -> None
    """Perform install."""
    # Executor(
    #     package.namespace,
    #     config=WorkflowConfig(ctx.config),
    # ).execute('package.install')
    ...


@task
def build(ctx):  # type: (Context) -> None
    """Perform build."""
    Executor(
        package.namespace,
        config=WorkflowConfig(ctx.config),
    ).execute('package.build')


@task
def unit_test(ctx):  # type: (Context) -> None
    """Perform unit-testing."""
    from pprint import pprint
    pprint(ctx.config.__dict__)
    # print(qa.namespace.task_names)
    try:
        Executor(
            qa.namespace,
            config=WorkflowConfig(ctx.config),
        ).execute('unit-tests.run')
    except Exception as err:
        print(err)


@task
def integration_test(ctx):  # type: (Context) -> None
    """Perform integration testing."""
    # Executor(.namespace, config=WorkflowConfig(ctx.config)).execute('')
    ...


@task
def system_test(ctx):  # type: (Context) -> None
    """Perform system testing."""
    # Executor(.namespace, config=WorkflowConfig(ctx.config)).execute('')
    ...


@task
def acceptance_test(ctx):  # type: (Context) -> None
    """Perform acceptance testing."""
    # Executor(.namespace, config=WorkflowConfig(ctx.config)).execute('')
    ...


@task
def publish(ctx):  # type: (Context) -> None
    """Publish package."""
    print(package.namespace.task_names)
    Executor(
        package.namespace,
        config=WorkflowConfig(ctx.config),
    ).execute('package.publish')


# project_config = config.ProjectConfig(
#     docs=asdict(DocsConfig()),
#     plugins=[
#         config.Plugin(
#             name='vcs',
#             driver_name='git',
#             driver_namespace='proman.workflows.vcs',
#         ),
#         config.Plugin(
#             name='sort-headers',
#             driver_name='isort',
#             driver_namespace='proman.workflows.formatter',
#         ),
#         config.Plugin(
#             name='format',
#             driver_name='black',
#             driver_namespace='proman.workflows.formatter',
#         ),
#         config.Plugin(
#             name='gpg',
#             driver_name='gpg',
#             driver_namespace='proman.workflows.pki',
#         ),
#         config.Plugin(
#             name='tls',
#             driver_name='tls',
#             driver_namespace='proman.workflows.pki',
#         ),
#     ]
# )
namespace = Collection(
    static_analysis,
    install,
    build,
    unit_test,
    acceptance_test,
    integration_test,
    system_test,
    publish,
)
# namespace.configure(asdict(project_config))
# namespace.load_collections()

__all__ = ['namespace']
