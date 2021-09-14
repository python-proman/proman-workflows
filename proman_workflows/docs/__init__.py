# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide documentation task-runner."""

import textwrap

from invoke import Context, task

from . import config


@task
def lint(ctx):  # type: (Context) -> None
    """Check code for documentation errors."""
    ctx.run('pydocstyle')


@task
def coverage(ctx):  # type: (Context) -> None
    """Ensure all code is documented."""
    ctx.run('docstr-coverage **/*.py')


@task(pre=[lint], post=[coverage])
def test(ctx):  # type: (Context) -> None
    """Test documentation build."""
    with ctx.cd(config.docs_dir):
        ctx.run('mkdocs build')


@task
def build(ctx):  # type: (Context) -> None
    """Build documentation site."""
    with ctx.cd(config.docs_dir):
        ctx.run('mkdocs build')


@task
def start(ctx, hostname='localhost', port=8001):  # type: (Context, str, int) -> None
    """Start docsite."""
    with ctx.cd(config.docs_dir):
        ctx.run(
            textwrap.dedent(
                f"""\
                mkdocs serve \
                --dev-addr={hostname}:{port} \
                --livereload
            """
            ),
            disown=True,
        )


@task
def stop(ctx):  # type: (Context) -> None
    """Stop docsite."""
    ctx.run('pkill mkdocs')
