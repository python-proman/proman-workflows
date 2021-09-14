# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

from typing import TYPE_CHECKING, Optional

from invoke import task

from .. import config

if TYPE_CHECKING:
    from invoke import Context


@task(iterator=['kind'])
def check(
    ctx,  # type: Context
    recursive=None,  # type: Optional[str]
    aggregate=None,  # type: Optional[str]
    number=None,  # type: Optional[str]
    configfile=None,  # type: Optional[str]
    profile=None,  # type: Optional[str]
    tests=None,  # type: Optional[str]
    skip=None,  # type: Optional[str]
    level=None,  # type: Optional[str]
    confidence=None,  # type: Optional[str]
    kind=None,  # type: Optional[str]
    msg_template=None,  # type: Optional[str]
    output=None,  # type: Optional[str]
    verbose=None,  # type: Optional[str]
    debug=None,  # type: Optional[str]
    silent=None,  # type: Optional[str]
    ignore_nosec=None,  # type: Optional[str]
    exclude=None,  # type: Optional[str]
    baseline=None,  # type: Optional[str]
    ini_path=None,  # type: Optional[str]
    exit_zero=None,  # type: Optional[str]
):  # type: (...) -> None
    """Perform static code analysis on imports."""
    args = []
    if recursive:
        args.append('--recursive')
    if aggregate:
        args.append(f"--aggregate {aggregate}")
    if number:
        args.append(f"--number {number}")
    if configfile:
        args.append(f"--configfile {configfile}")
    if profile:
        args.append(f"--profile {profile}")
    if tests:
        args.append(f"--tests {tests}")
    if skip:
        args.append(f"--skip {skip}")
    if level:
        args.append('--level')
    if confidence:
        args.append('--confidence')
    if kind:
        args.append(f"--format {','.join(kind)}")
    if msg_template:
        args.append(f"--msg-template {msg_template}")
    if output:
        args.append(f"--output {output}")
    if verbose:
        args.append('--verbose')
    if debug:
        args.append('--debug')
    if silent:
        args.append('--silent')
    if ignore_nosec:
        args.append('--ignore-nosec')
    if exclude:
        args.append(f"--exclude '{','.join(exclude)}'")
    if baseline:
        args.append(f"--baseline {baseline}")
    if ini_path:
        args.append(f"--ini {ini_path}")
    if exit_zero:
        args.append('--exit-zero')
    with ctx.cd(config.webapp_dir):
        ctx.run(f"safety check {' '.join(args)}")
