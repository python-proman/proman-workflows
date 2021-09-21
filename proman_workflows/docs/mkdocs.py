# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide documentation task-runner."""

import textwrap
from typing import TYPE_CHECKING, Optional

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def build(
    ctx,  # type: Context
    clean=False,  # type: bool
    configfile=None,  # type: Optional[str]
    strict=False,  # type: bool
    theme=None,  # type: Optional[str]
    use_directory_urls=None,  # type: Optional[str]
    path=None,  # type: Optional[str]
    quiet=False,  # type: bool
    verbose=False,  # type: bool
):  # type: (...) -> None
    """Build documentation site."""
    args = []
    if clean is not None:
        args.append('--clean' if clean else '--dirty')
    if configfile:
        args.append(f"--config-file {configfile}")
    if strict:
        args.append('--strict')
    if theme:
        if theme in ['readthedocs', 'material', 'mkdocs']:
            args.append(f"--theme {theme}")
        else:
            raise Exception(f"{theme} is not a supported mkdocs theme")
    if use_directory_urls is not None:
        args.append(
            '--use-directory-urls'
            if use_directory_urls else '--no-directory-urls'
        )
        args.append(f"--site-dir {path}")
    if quiet:
        args.append('--quiet')
    if verbose:
        args.append('--verbose')

    with ctx.cd(ctx.docs_dir):
        ctx.run(f"mkdocs build {' '.join(args)}")


@task
def start(
    ctx,
    hostname='localhost',
    port=8001
):  # type: (Context, str, int) -> None
    """Start docsite."""
    with ctx.cd(ctx.docs_dir):
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


namespace = Collection(build, start, stop)
