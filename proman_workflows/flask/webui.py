# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Static Content Task-Runner."""

from typing import Optional

from invoke import Context, task

from .. import config


@task
def install(
    ctx, path=config.webui_dir, also='dev'
):  # type: (Context, str, str) -> None
    """Install WebUI dependencies."""
    with ctx.cd(path):
        ctx.run(f"npm install --also={also}")


@task(pre=[install])
def build(ctx, path=config.webui_dir):  # type: (Context, str) -> None
    """Build static content."""
    with ctx.cd(path):
        ctx.run('npm run build')


@task
def start(
    ctx, host=None, port=8000, browser=False, path=config.webui_dir
):  # type: (Context, Optional[str], int, bool, str) -> None
    """Start webui development."""
    args = []
    if browser:
        args.append('--open')
    if host:
        args.append(f"--host={host}")
    if port:
        args.append(f"--port={port}")
    with ctx.cd(path):
        print("npx vue-cli-service serve {}".format(' '.join(args)))
        ctx.run(
            "npx vue-cli-service serve",  # {}".format(' '.join(args)),
            asynchronous=True,
        )


@task
def stop(ctx):  # type: (Context) -> None
    """Stop WebUI development."""
    ctx.run('pkill npm')
