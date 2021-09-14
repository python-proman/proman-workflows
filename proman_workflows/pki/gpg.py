"""Provide signature capability using GnuPG."""

import os
from typing import TYPE_CHECKING, Optional

from gnupg import GPG
from invoke import task

if TYPE_CHECKING:
    from gnupg import GenKey, ListKeys
    from invoke import Context

gpg = GPG(gnupghome=os.path.join(os.path.expanduser('~'), '.gnupg'))


@task
def list_keys(
    ctx, secret=False, keys=None, sigs=False
):  # type: (Context, bool, Optional[str], bool) -> ListKeys
    """List GPG keys."""
    keys = gpg.list_keys(secret=secret, keys=keys, sigs=sigs)
    return keys


@task(iterable=['query'])
def get_key(ctx, query):  # type: (Context, str) -> GenKey
    """Get GPG key."""
    keys = []
    for key in list_keys(ctx):
        for q in query:
            if '=' in q:
                k, v = q.split('=')
                if key[k] == v:
                    keys.append(key)
            elif q in key:
                keys.append(key)
    return keys


@task
def generate_key(
    ctx,  # type: Context
    name=None,  # type: Optional[str]
    email=None,  # type: Optional[str]
    comment=None,  # type: Optional[str]
    password=None,  # type: Optional[str]
    key_type=None,  # type: Optional[str]
    key_length=None,  # type: Optional[int]
    expire_date=None,  # type: Optional[int]
    no_protection=None,  # type: Optional[str]
):  # type: (...) -> GenKey
    """Generate GPG key."""
    input_data = gpg.gen_key_input(
        name_real=name,
        name_email=email,
        name_comment=comment,
        passphrase=password,
        key_type=key_type,
        key_length=key_length,
        expire_date=expire_date,
        no_protection=no_protection,
    )
    key = gpg.gen_key(input_data)
    return key


@task
def export_key(
    ctx, key, keypath, secret=False
):  # type: (Context, str, str, bool) -> None
    """Export an armored GPG key."""
    ascii_armored_keys = gpg.export_keys(key, secret)
    with open(f"{key}.asc", 'w') as f:
        f.write(ascii_armored_keys)
