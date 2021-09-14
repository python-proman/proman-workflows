# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide App Task-Runner."""

import os
import textwrap

from invoke import Context, task

from .. import config


def build(ctx, path='.'):  # type: (Context, str) -> None
    """Build docker image."""
    ctx.run(
        f"""\
        pipenv lock \
        --requirements > {config.webapp_dir}/requirements.txt
    """
    )
    with ctx.cd(config.webapp_dir):
        ctx.run(f"docker build {path}")


@task
def start(
    ctx, hostname='localhost', port=8080, workers=4
):  # type: (Context, str, int, int) -> None
    """Start webapp."""
    with ctx.cd(config.webapp_dir):
        ctx.run(
            textwrap.dedent(
                f"""\
                gunicorn app:app \
                --pid={os.getcwd()}/.pid \
                --bind={hostname}:{port} \
                --workers={workers} \
                --reload
            """
            ),
            disown=True,
        )


@task
def stop(ctx):  # type: (Context) -> None
    """Stop webapp."""
    ctx.run('pkill gunicorn')
