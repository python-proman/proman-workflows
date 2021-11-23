# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Implement software testing life-cycle."""

import logging
# import os
from dataclasses import asdict
from pprint import pprint
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
from proman_workflows.config import (
    Job,
    # Plugin,
    Phase,
    ProjectConfig,
    WorkflowConfig
)

if TYPE_CHECKING:
    from invoke import Context

logging.getLogger(__name__).addHandler(logging.NullHandler())


@task
def execute_jobs(ctx, task_name):  # type: (Context, str) -> None
    config = [p for p in ctx.phases if p['name'] == task_name][0]
    jobs = [(j['command'], j['args']) for j in config['jobs']]
    try:
        Executor(
            qa.namespace,
            config=WorkflowConfig(ctx.config),
        ).execute(*jobs)
    except Exception as err:
        print(err)


@task
def static_analysis(ctx):  # type: (Context) -> None
    """Perform static code analysis."""
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
    # print(qa.namespace.task_names)
    execute_jobs(ctx, task_name='unit-test')


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


project_config = ProjectConfig(
    # plugins=[
    #     Plugin(
    #         name='poetry',
    #         driver_name='package',
    #         driver_namespace='proman_workflows.package.poetry',
    #     ),
    #     Plugin(
    #         name='vcs',
    #         driver_name='git',
    #         driver_namespace='proman.workflows.vcs',
    #     ),
    #     Plugin(
    #         name='sort-headers',
    #         driver_name='isort',
    #         driver_namespace='proman.workflows.formatter',
    #     ),
    #     Plugin(
    #         name='format',
    #         driver_name='black',
    #         driver_namespace='proman.workflows.formatter',
    #     ),
    #     Plugin(
    #         name='unit-tests',
    #         driver_name='pytest',
    #         driver_namespace='proman.workflows.unit_tests',
    #     ),
    # ],
    phases=[
        Phase(
            name='install',
            plugins=['poetry'],
            jobs=[Job(command='poetry.install', args={})],
        ),
        Phase(
            name='static-analysis',
            # plugins=[],
            jobs=[Job(command='', args={})],

        ),
        Phase(
            name='build',
            plugins=['poetry'],
            jobs=[Job(command='poetry.build', args={})],
        ),
        Phase(
            name='unit-test',
            # plugins=[],
            jobs=[Job(command='unit-tests.run', args={})],
        ),
        Phase(
            name='acceptance-test',
            # plugins=[],
            jobs=[Job(command='', args={})],
        ),
        Phase(
            name='integration-test',
            # plugins=[],
            jobs=[Job(command='', args={})],
        ),
        Phase(
            name='system-test',
            # plugins=[],
            jobs=[Job(command='', args={})],
        ),
        Phase(
            name='publish',
            plugins=['poetry'],
            jobs=[Job(command='poetry.publish', args={})],
        )
    ]
)
namespace = Collection(
    install,
    static_analysis,
    build,
    unit_test,
    acceptance_test,
    integration_test,
    system_test,
    publish,
)
pprint(asdict(project_config))
namespace.configure(asdict(project_config))
# namespace.load_collections()

__all__ = ['namespace']
