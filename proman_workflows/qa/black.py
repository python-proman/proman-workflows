# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

from typing import TYPE_CHECKING, Optional

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def run(
    ctx,  # type: Context
    code=None,  # type: Optional[str]
    line_length=79,  # type: int
    target_version=None,  # type: Optional[str]
    pyi=None,  # type: Optional[str]
    skip_string_normalization=False,  # type: bool
    skip_magic_trailing_comma=None,  # type: Optional[bool]
    check=None,  # type: Optional[bool]
    diff=None,  # type: Optional[bool]
    color=None,  # type: Optional[bool]
    execution=None,  # type: Optional[bool]
    required_version=None,  # type: Optional[str]
    include=None,  # type: Optional[str]
    exclude=None,  # type: Optional[str]
    extend_exclude=None,  # type: Optional[str]
    force_exclude=None,  # type: Optional[str]
    stdin_filename=None,  # type: Optional[str]
    quiet=None,  # type: Optional[bool]
    verbose=None,  # type: Optional[bool]
    version=None,  # type: Optional[bool]
    config=None,  # type: Optional[str]
):  # type: (...) -> None
    """Lint or format using black."""
    args = []
    if code:
        args.append(f"--code {code}")
    if line_length:
        args.append(f"--line-length {line_length}")
    if target_version:
        args.append('--target-version')
    if pyi:
        args.append('--pyi')
    if skip_string_normalization:
        args.append('--skip-string-normalization')
    if skip_magic_trailing_comma:
        args.append('--skip-magic-trailing-comma')
    if check:
        args.append('--check')
    if diff:
        args.append('--diff')
    if color is not None:
        args.append('--color' if color else '--no-color')
    if execution == 'fast':
        args.append('--fast')
    if execution == 'safe':
        args.append('--safe')
    if required_version:
        args.append(f"--required-version {required_version}")
    if include:
        args.append(f"--include {include}")
    if exclude:
        args.append(f"--exclude {exclude}")
    if extend_exclude:
        args.append(f"--extend-exclude {extend_exclude}")
    if force_exclude:
        args.append(f"--force-exclude {force_exclude}")
    if stdin_filename:
        args.append(f"--stdin-filename {stdin_filename}")
    if quiet:
        args.append('--quiet')
    if verbose:
        args.append('--verbose')
    if version:
        args.append('--version')
    if config:
        args.append(f"--config {config}")
    ctx.run(f"black {' '.join(args)}")


namespace = Collection(run)
