# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Implement software testing life-cycle."""

from dataclasses import asdict
from pprint import pprint  # noqa
from typing import TYPE_CHECKING

from invoke import Executor, task

# TODO: switch to executor
from proman_workflows import __title__, __version__, WorkflowProgram
from proman_workflows.config import Plugin, ProjectConfig, WorkflowConfig
from proman_workflows.collection import Collection

from . import mock

if TYPE_CHECKING:
    from invoke import Context


@task
def job(ctx):  # type: (Context) -> None
    """Perform static code analysis."""
    # if 'plugins' in ctx:
    #     pprint(ctx.plugins)
    # else:
    #     pprint({'mock-vars': ctx.config.__dict__['_config']})
    # print(mock.namespace.task_names)
    pprint(ctx.config.__dict__)
    mock.namespace.load_collections(plugins=ctx.plugins)
    Executor(
        mock.namespace,
        config=WorkflowConfig(ctx.config)
    ).execute('mock.run')


project_config = ProjectConfig(
    plugins=[
        Plugin(
            name='mock',
            driver_name='update',
            driver_namespace='proman.workflows.mock',
        ),
    ]
)
# print(asdict(project_config))
namespace = Collection(job)
namespace.configure(asdict(project_config))
namespace.configure({'inherited': 'root'})
# namespace.load_collections()

workflow = WorkflowProgram(
    name=__title__,
    namespace=namespace,
    binary='workflow',
    binary_names=['workflow'],
    # config_class=WorkflowConfig,
    version=__version__,
)

__all__ = ['namespace', 'workflow']
