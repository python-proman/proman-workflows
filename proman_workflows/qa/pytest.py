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
    capture=None,  # type: Optional[str]
    debugger=None,  # type: Optional[str]
    durations=None,  # type: Optional[int]
    durations_min=None,  # type: Optional[int]
    maxfail=None,  # type: Optional[int]
):  # type: (...) -> None
    """Perform unit tests."""
    args = []
    if capture:
        args.append(f"--capture={capture}")
    if debugger:
        args.append('--pdb')
    if durations:
        args.append(f"--durations={durations}")
    if durations_min:
        args.append(f"--durations-min={durations_min}")
    if maxfail:
        args.append(f"--maxfail={maxfail}")
    with ctx.cd(ctx.working_dir):
        ctx.run(f"pytest {' '.join(args)}")


@task
def coverage(
    ctx, project_dir, report=None
):  # type: (Context, str, Optional[str]) -> None
    """Perform coverage checks for tests."""
    args = [f"--cov={project_dir}"]
    if report:
        args.append(f"--cov-report={report}")
    with ctx.cd(ctx.working_dir):
        ctx.run(f"pytest {' '.join(args)}")


namespace = Collection(run)
