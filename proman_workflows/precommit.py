# type: ignore
"""Provide pre-commit setup."""

from typing import TYPE_CHECKING, Optional

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def update(
    ctx, package=None, force=False
):  # type: (Context, Optional[str], bool) -> None
    """Update package."""
    print('yeppers')


tasks = Collection(update)
