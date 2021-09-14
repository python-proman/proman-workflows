# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Validation Task-Runner."""

import os
import shutil

from invoke import Context, task


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
