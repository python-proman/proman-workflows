"""Provide signature capability using GnuPG."""

import os
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from gnupg import GPG
from invoke import Collection, task

from proman_workflows.config import GPGConfig

if TYPE_CHECKING:
    from gnupg import GenKey, ListKeys
    from invoke import Context


@task
def agent(
    ctx,  # type: Context
    daemon=False,  # type: bool
    supervised=False,  # type: bool
    verbose=False,  # type: bool
    quiet=False,  # type: bool
    sh=False,  # type: bool
    csh=False,  # type: bool
    options=None,  # type: Optional[str]
    dettach=True,  # type: bool
    log_file=None,  # type: Optional[str]
    pinentry_program=None,  # type: Optional[str]
    allow_loopback_pinentry=True,  # type: bool
    allow_emacs_pinentry=True,  # type: bool
    scdaemon_program=None,  # type: Optional[str]
    disable_scdaemon=True,  # type: bool
    extra_socket=None,  # type: Optional[int]
    keep_tty=True,  # type: bool
    keep_display=False,  # type: bool
    default_cache_ttl=None,  # type: Optional[int]
    ignore_cache_for_signing=False,  # type: bool
    allow_external_cache=True,  # type: bool
    allow_mark_trusted=True,  # type: bool
    allow_preset_passphrase=False,  # type: bool
    enable_ssh_support=False,  # type: bool
    ssh_fingerprint_digest=None,  # type: Optional[str]
):  # type: (...) -> None
    """Start gpg agent."""
    args = []
    if daemon:
        args.append('--daemon')
    if supervised:
        args.append('--supervised')
    if verbose:
        args.append('--verbose')
    if quiet:
        args.append('--quiet')

    # shell
    if sh:
        args.append('--sh')
    if csh:
        args.append('--csh')

    if keep_tty:
        args.append('--keep-tty')
    if keep_display:
        args.append('--keep-display')

    if not dettach:
        args.append('--no-detach')
    if log_file:
        args.append('--log-file')

    # setup pin entry UI application
    if pinentry_program:
        args.append(f"--pinentry-program {pinentry_program}")
        if not allow_loopback_pinentry:
            args.append('--no-allow-loopback-pinentry')
        if allow_emacs_pinentry:
            args.append('--allow-emacs-pinentry')

    # setup smartcard integration
    if disable_scdaemon:
        args.append('--disable-scdaemon')
    elif scdaemon_program:
        args.append(f"--scdaemon-program {scdaemon_program}")

    if extra_socket:
        args.append(f"--extra-socket {extra_socket}")

    # cache
    if default_cache_ttl:
        args.append(f"--default-cache-ttl {default_cache_ttl}")
    if ignore_cache_for_signing:
        args.append('--ignore-cache-for-signing')
    if not allow_external_cache:
        args.append('--no-allow-external-cache')

    if not allow_mark_trusted:
        args.append('--no-allow-mark-trusted')
    if allow_preset_passphrase:
        args.append('--allow-preset-passphrase')
    if enable_ssh_support:
        args.append('--enable-ssh-support')
        if ssh_fingerprint_digest:
            args.append(f"--ssh-fingerprint-digest {ssh_fingerprint_digest}")

    # gpg options
    if options:
        args.append(f"--options '{','.join(options)}'")
    ctx.run(f"gpgconf --launch gpg-agent {' '.join(args)}")


@task
def config(
    ctx,  # type: Context
    gnupghome=os.path.join(os.path.expanduser('~'), '.gnupg'),  # type: str
    keyring=None,  # type: Optional[str]
    secret_keyring=None,  # type: Optional[str]
):  # type: (...) -> None
    """Get gpg instance."""
    if 'gpg' not in ctx:
        ctx.__gpg = GPG(
            gnupghome=gnupghome,
            keyring=keyring,
            secret_keyring=secret_keyring
        )


@task(pre=[config])
def list_keys(
    ctx, secret=False, keys=None, sigs=False
):  # type: (Context, bool, Optional[str], bool) -> ListKeys
    """List GPG keys."""
    keys = ctx.__gpg.list_keys(secret=secret, keys=keys, sigs=sigs)
    print([k['keyid'] for k in keys])
    return keys


@task(pre=[config])
def get_key(
    ctx, query, secret=False, sigs=False
):  # type: (Context, str, bool, bool) -> List[GenKey]
    """Get GPG key."""
    keys = []
    for key in list_keys(ctx, secret=secret, sigs=sigs):
        if '=' in query:
            k, v = query.split('=')
            if key[k] == v:
                keys.append(key)
        elif query in key.values():
            keys.append(key)
    return keys


@task(pre=[config])
def export_key(
    ctx, key, keypath, secret=False
):  # type: (Context, str, str, bool) -> None
    """Export an armored GPG key."""
    ascii_armored_keys = ctx.__gpg.export_keys(key, secret)
    with open(f"{key}.asc", 'w') as f:
        f.write(ascii_armored_keys)


@task(pre=[config])
def delete_key(
    ctx,
    query,
    # secret=True,
    sigs=False,
    passphrase='',
    expect_passphrase=True,
):  # type: (Context, str, bool, Optional[str], bool) -> None
    """Delete GPG key."""
    for secret in (True, False):
        keys = get_key(ctx, query, secret, sigs)
        for key in keys:
            ctx.__gpg.delete_keys(
                [x['fingerprint'] for x in keys],
                secret=secret,
                passphrase=passphrase,
                expect_passphrase=expect_passphrase,
            )


@task(pre=[config])
def gen_key(
    ctx,  # type: Context
    name,  # type: str
    email,  # type: str
    password,  # type: str
    comment='generated by proman',  # type: Optional[str]
    key_type='RSA',  # type: str
    key_length=None,  # type: Optional[int]
    key_curve=None,  # type: Optional[str]
    key_usage=None,  # type: Optional[str]
    expire_date='1y',  # type: str
    subkey=None,  # type: Optional[bool]
):  # type: (...) -> GenKey
    """Generate GPG key."""
    # TODO: default to subkey if primary key exists
    key_settings: Dict[str, Any] = {
        'subkey_type' if subkey else 'key_type': key_type,
    }
    if key_length and key_type in ['DSA', 'ELG', 'RSA']:
        key_settings['subkey_length' if subkey else 'key_length'] = key_length
    if key_curve and key_type in ['ECDH', 'ECDSA', 'EDDSA']:
        # [
        #     'curve25519',  # cv25519, or ed25519
        #     'p256',
        #     'p384',
        #     'p521',
        #     'secp256k1'
        #     # 'brainpoolP256r1',
        #     # 'brainpoolP384r1',
        #     # 'brainpoolP512r1',
        # ]
        key_settings['subkey_curve' if subkey else 'key_curve'] = key_curve
    # if key_usage and key_type in ['auth', 'cert', 'encrypt', 'sign']:
    #     key_settings['subkey_usage' if subkey else 'key_usage'] = key_usage

    key_settings['expire_date'] = expire_date
    key_settings['no_protection'] = True if password == '' else False

    input_data = ctx.__gpg.gen_key_input(
        name_real=name,
        name_email=email,
        name_comment=comment,
        passphrase=password,
        **key_settings,
    )
    # print('input', input_data)
    key = ctx.__gpg.gen_key(input_data)
    print('key', key)
    return key


settings = GPGConfig()
namespace = Collection()
namespace.configure(
    {
        'settings': asdict(settings),
        'signing': {
            'developers': {
                'required': True,
            },
            'packaging': {
                'required': True,
            },
        },
    }
)
namespace.add_task(config)
namespace.add_task(list_keys)
namespace.add_task(get_key)
namespace.add_task(delete_key)
namespace.add_task(export_key)
namespace.add_task(gen_key)
