# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Validation Task-Runner."""

import os
import shutil
from typing import TYPE_CHECKING, Optional

from invoke import task

if TYPE_CHECKING:
    from invoke import Context


@task
def mkdir(ctx, path):  # type: (Context, str) -> None
    """Make directory path."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as err:
        print(f"unable to download github release due to: {err}")


@task
def rmdir(ctx, path):  # type: (Context, str) -> None
    """Remove directory path."""
    try:
        shutil.rmtree(path)
    except OSError as err:
        print(f"unable to delete direcotry path due to: {err}")


@task(iterable=['path'])
def clean(
    ctx,  # type: Context
    path=None,  # type: Optional[str]
    mindepth=None,  # type: Optional[int]
    maxdepth=None,  # type: Optional[int]
):  # type: (...) -> None
    """Clean project dependencies and build."""
    args = []
    if not path:
        paths = [
            '__pycache__',
            '.mypy_cache',
            'dist',
            '*.pyc',
        ]
    if mindepth:
        args.append(f"-mindepth {mindepth}")
    if maxdepth:
        args.append(f"-maxdepth {maxdepth}")
    for path in paths:
        ctx.run(
            "find . %s -exec rm -rf {} +"
            % (' '.join([f"-name {path}"] + args))
        )
