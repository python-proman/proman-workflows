# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide documentation task-runner."""

from typing import TYPE_CHECKING

from invoke import task

from ..collection import Collection

if TYPE_CHECKING:
    from invoke import Context


@task
def lint(ctx):  # type: (Context) -> None
    """Check code for documentation errors."""
    ctx.run('pydocstyle')


@task
def coverage(ctx):  # type: (Context) -> None
    """Ensure all code is documented."""
    ctx.run('docstr-coverage **/*.py')


namespace = Collection()
namespace.configure(
    {
        '_collections': [
             {
                'name': 'site',
                'driver_name': 'mkdocs',
                'driver_namespace': 'proman.workflow.docs'
             }
        ]
    }
)
namespace.load_collections()
namespace.add_task(lint)
namespace.add_task(coverage)
