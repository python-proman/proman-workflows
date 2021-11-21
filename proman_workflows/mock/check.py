# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Build packages using flit."""

from pprint import pprint
from typing import TYPE_CHECKING, Optional

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def run(ctx, foo=None):  # type: (Context, Optional[str]) -> None
    """Provide mock tool run."""
    # print(foo or ctx.foo)
    pprint({'check-vars': ctx.config.__dict__['_config']})


namespace = Collection(run)
namespace.configure(
    {
        'foo': 'namespace',
        'check': 'stub',
    }
)
