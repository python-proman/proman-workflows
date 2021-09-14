# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide package task-runner."""

# import importlib
from typing import TYPE_CHECKING, Optional

from invoke import Collection, task

from . import poetry, twine

if TYPE_CHECKING:
    from invoke import Context


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
            "find . %s -exec rm -rf {} +" % (
                ' '.join([f"-name {path}"] + args)
            )
        )


@task
def build(
    ctx,
    kind='wheel',
    outdir=None,
    skip_dependency_check=False,
    no_isolation=False,
):  # type: (Context, str, Optional[str], bool, bool) -> None
    """Build package."""
    args = []
    if kind == 'wheel':
        args.append('--wheel')
    elif kind == 'sdist':
        args.append('--sdist')
    else:
        raise Exception('cannot build unknown package format')
    if outdir:
        args.append(f"--outdir={outdir}")
    if skip_dependency_check:
        args.append('--skip-dependency-check')
    if no_isolation:
        args.append('--no-isolation')
    ctx.run(f"{ctx.python_path} -m build {' '.join(args)}")


@task
def install(
    ctx,  # type: Context
    dev=True,  # type: bool
    editable=True,  # type: bool
    remove_untracked=None,  # type: Optional[str]
    extras=None,  # type: Optional[str]
):  # type: (...) -> None
    """Install package locally."""
    poetry.install(
        ctx,
        dev=dev,
        editable=editable,
        remove_untracked=remove_untracked,
        extras=extras,
    )


@task
def publish(
    ctx,  # type: Context
    repository=None,  # type: Optional[str]
    repository_url=None,  # type: Optional[str]
    sign=False,  # type: bool
    sign_with=None,  # type: Optional[str]
    identity=None,  # type: Optional[str]
    username=None,  # type: Optional[str]
    password=None,  # type: Optional[str]
    comment=None,  # type: Optional[str]
    cert_path=None,  # type: Optional[str]
    client_cert_path=None,  # type: Optional[str]
):  # type: (...) -> None
    """Publich package to repository."""
    twine.publish(
        ctx,
        repository=repository,
        repository_url=repository_url,
        sign=sign,
        sign_with=sign_with,
        identity=identity,
        username=username,
        password=password,
        comment=comment,
        cert_path=cert_path,
        client_cert_path=client_cert_path,
    )


@task
def version(
    ctx,
    part=None,
    tag=False,
    commit=False,
    message=None,
):  # type: (Context, Optional[str], bool, bool, Optional[str]) -> None
    """Update project version and apply tags."""
    version = ctx.spec['tool']['poetry']['version']
    if (
        'dev' in version
        or ('a' in version or 'alpha' in version)
        or ('b' in version or 'beta' in version)
        or 'rc' in version
    ):
        part = 'build'
    else:
        part = 'patch'

    args = [part]
    if commit:
        args.append('--commit')
    else:
        args.append('--dry-run')
        args.append('--allow-dirty')
        args.append('--verbose')
        print('Add "--commit" to actually bump the version.')
    if tag or message:
        args.append('--tag')
        if message:
            args.append(f"--tag-message '{message}'")
    ctx.run(f"bumpversion {' '.join(args)}")


build_tasks = Collection(twine, clean, build, version)
# build_tasks.add_collection(flit, name='flit')
# build_tasks.add_collection(poetry, name='poetry')
# build_tasks.add_collection(twine, name='twine')
