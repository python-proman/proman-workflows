# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Check if variable is overidden by plugin."""

from pprint import pprint  # noqa
from typing import TYPE_CHECKING, Optional

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def run(ctx, foo=None):  # type: (Context, Optional[str]) -> None
    """Provide mock tool run."""
    print(ctx.inherited)
    print(foo or ctx.foo)
    # pprint(ctx.config.__dict__)


namespace = Collection(run)
namespace.configure({'foo': 'bar'})
