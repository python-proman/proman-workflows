# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Implement software testing life-cycle."""

# from dataclasses import asdict
from pprint import pprint
from typing import TYPE_CHECKING

from invoke import Executor, task

# TODO: switch to executor
from proman_workflows import (
    __title__,
    __version__,
    mock,
    WorkflowProgram,
)
from proman_workflows.config import ProjectConfig, WorkflowConfig
from proman_workflows.collection import Collection

if TYPE_CHECKING:
    from invoke import Context


@task
def job(ctx):  # type: (Context) -> None
    """Perform static code analysis."""
    if 'plugins' in ctx:
        pprint(ctx.plugins)
    else:
        pprint({'mock-vars': ctx.config.__dict__['_config']})
    # print(mock.namespace.task_names)
    Executor(
        mock.namespace,
        # config=ctx.config
        config=WorkflowConfig(ctx.config)
    ).execute('mock.run')


project_config = ProjectConfig()
#     plugins=[
#         config.Plugin(
#             name='vcs',
#             driver_name='git',
#             driver_namespace='proman.workflows.vcs',
#         ),
#     ]
# )
# print(asdict(project_config))
namespace = Collection(job)
# namespace.configure(asdict(project_config))
namespace.configure({'mock': 'stub'})
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
