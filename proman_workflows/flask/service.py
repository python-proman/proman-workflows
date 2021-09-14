# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Build Task-Runner."""

from passlib.pwd import genword
from invoke import Context, task

from . import compose
from . import filesystem
from . import certs


@task
def start(ctx, certs_path='./nginx/certs'):  # type: (Context, str) -> None
    """Start all services."""
    certs.setup(ctx)
    filesystem.mkdir(ctx, certs_path)
    certs.generate(
        ctx,
        name=['spades.local', 'localhost'],
        key=f"{certs_path}/spades.key",
        cert=f"{certs_path}/spades.crt",
    )
    env = {
        'POSTGRESQL_PASSWORD': genword(entropy=56, length=128),
        'REDIS_PASSWORD': genword(entropy=56, length=128),
    }
    compose.start(ctx, files=[], env=env)


@task
def stop(ctx, certs_path='./nginx/certs'):  # type: (Context, str) -> None
    """Stop all services."""
    compose.stop(ctx)
    certs.cleanup(ctx)
    filesystem.rmdir(ctx, certs_path)
