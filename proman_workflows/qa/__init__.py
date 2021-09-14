# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

from typing import Optional

from invoke import Context, task

from .. import config


@task
def style(ctx):  # type: (Context) -> None
    """Format project source code to PEP-8 standard."""
    # args = ['--skip-string-normalization']
    with ctx.cd(config.webapp_dir):
        ctx.run('isort --atomic **/*.py')
        ctx.run('autopep8 --in-place --recursive .')


@task
def lint(ctx):  # type: (Context) -> None
    """Check project source code for linting errors."""
    with ctx.cd(config.webapp_dir):
        ctx.run('flake8')


@task
def type_check(ctx, path='.'):  # type: (Context, str) -> None
    """Check project source types."""
    with ctx.cd(config.webapp_dir):
        ctx.run("mypy {}".format(path))


@task
def unit_test(ctx, capture=None):  # type: (Context, Optional[str]) -> None
    """Perform unit tests."""
    args = []
    if capture:
        args.append('--capture=' + capture)
    with ctx.cd(config.webapp_dir):
        ctx.run("pytest {}".format(' '.join(args)))


@task
def static_analysis(ctx):  # type: (Context) -> None
    """Perform static code analysis on imports."""
    with ctx.cd(config.webapp_dir):
        ctx.run('safety check')
        ctx.run('bandit -r spades')


@task
def coverage(ctx, report=None):  # type: (Context, Optional[str]) -> None
    """Perform coverage checks for tests."""
    args = ['--cov=spades']
    if report:
        args.append('--cov-report={}'.format(report))
    with ctx.cd(config.webapp_dir):
        ctx.run("pytest {} ./tests/".format(' '.join(args)))


@task(pre=[style, lint, unit_test, static_analysis, coverage])
def test(ctx):  # type: (Context) -> None
    """Run all tests."""
    pass
