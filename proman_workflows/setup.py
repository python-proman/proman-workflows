# -*- coding: utf-8 -*-
"""Provide setup capability."""

from typing import Optional
from proman_workflows.git import hooks
from invoke import Collection, Context, task


@task
def update(ctx, package=None, force=False):
    # type: (Context, Optional[str], bool) -> None
    """Update example."""
    print('yeppers')


@task
def commit_message(ctx, path='proman_workflows/templates/gitmessage.j2'):
    # type: (Context, str) -> None
    """Provide conventional commit directions."""
    pass


tasks = Collection().from_module(hooks)
