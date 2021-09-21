# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

from typing import TYPE_CHECKING

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def run(ctx):  # type: (Context) -> None
    """Format project headers to PEP8 standards."""
    with ctx.cd(ctx.working_dir):
        ctx.run('isort --atomic **/*.py')


namespace = Collection(run)
