# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide project initialization."""

import logging
import os
from typing import TYPE_CHECKING, Any, Dict

# import keyring
import pyinputplus as pyip
from invoke import Collection, task

from . import git

# from .config import GlobalConfig
from .pki import gpg

if TYPE_CHECKING:
    from invoke import Context
    from gpg import GenKey


def create_signingkey(ctx, name, email):  # type: (Context, str, str) -> GenKey
    """Create a signing key."""
    password = pyip.inputPassword('Enter GPG password: ', limit=255)
    # get comment

    res = pyip.inputYesNo('Perform adanced GPG setup (y/n): ')
    if res == 'yes':
        key_type = pyip.inputMenu(
            [
                'RSA',
                'ElGamal',
                'DSA',
                'ECDH',
                'ECDSA',
                'EdDSA',
            ],
            prompt='Select GPG key type:\n',
            default='EdDSA',
            numbered=True,
        )
        # key_length = pyip.inputInt('Enter key length: ')
        expire_date = pyip.inputStr(
            prompt='Enter expiration date: ',
            allowRegexes=[r'^(0|([\d]{1,4}[d|w|m|y]))$'],
            default='1y',
        )
        print(expire_date)

    key = gpg.gen_key(
        ctx,
        name=name,
        email=email,
        password=password,
        comment='primary',
        key_type=key_type,
        key_length=4096,
        expire_date='1y',
        subkey=False,
    )
    return key


def setup_gitconfig(ctx, update):  # type: (Context, bool) -> Dict[str, Any]
    """Ensure version control system is setup."""
    print('Check git user info is setup.', end='\n\n')
    gitconfig = git.config(ctx, scope='global')

    # select gpg if found else generate gpg key
    # setup gpg commit signing
    # setup gpg package signing

    if 'user' not in gitconfig['sections']:
        print('Verfying git user is defined...', end=' ')

    # if not config.retrieve('.gpg.signingkey'):
    try:
        print('Verfying git user.name is defined...', end=' ')
        name = gitconfig['sections']['user']['name']
        print('found')
    except Exception as err:
        logging.info(err)
        print('missing', end='\n\n')
        name = pyip.inputStr('Enter git user.name: ', limit=255)
        gitconfig['sections']['user']['name'] = name

    try:
        print('Verfying git user.email is defined...', end=' ')
        email = gitconfig['sections']['user']['email']
        print('found')
    except Exception as err:
        logging.info(err)
        print('missing', end='\n\n')
        email = pyip.inputEmail('Enter git user.email: ', limit=255)
        gitconfig['sections']['user']['email'] = email

    try:
        print('Verfying git user.sigingkey is defined...', end=' ')
        signingkey = gitconfig['sections']['user']['signingkey']
        print('found')
    except Exception as err:
        logging.info(f"{err}: no gpg signingkey defined")
        print('missing', end='\n\n')

        choices = ['Create a new subkey', 'Skip']
        gpg_keys = gpg.list_keys(ctx, secret=False, keys=None, sigs=False)
        if gpg_keys != []:
            print(
                'A GPG key was found but user.signingkey is undefined:',
                end='\n\n'
            )
            choices.insert(1, 'Choose an existing key')

        res = pyip.inputMenu(
            choices=choices,
            prompt=(
                'Would you like to create a key or use an existing one:\n'
            ),
            numbered=True
        )

        signingkey = None
        if res == 'Create a new subkey':
            signingkey = create_signingkey(ctx, name, email)

        elif res == 'Choose an existing key':
            selection = pyip.inputMenu(
                [f"{k['keyid']}:<{k['uids'][0]}>" for k in gpg_keys],
                prompt='\nSelect GPG key:\n',
                numbered=True,
            )
            signingkey = selection.split(':')[0]

        if signingkey:
            gitconfig['sections']['user']['signingkey'] = signingkey

    # setup keyring secrets
    if not hasattr(ctx, 'gpg'):
        ctx.gpg = dict()

    # if not keyring.get_password(f"{name}-signingkey", signingkey):
    #     keyring.set_password(f"{name}-signingkey", signingkey, password)

    # ctx.gpg.signingkey = signingkey
    # ctx.gpg.password = password

    # config.create('.gpg.signingkey', ctx.gpg.signingkey)
    # from pprint import pprint
    # pprint(ctx.config['gpg'])

    git.dump_config(
        ctx,
        gitconfig,
        template_name='gitconfig',
        dest=os.path.join(os.path.expanduser('~'), '.gitconfig'),
        update=update,
    )
    return gitconfig


def setup_gitignore(ctx):  # type: (Context) -> None
    """Check gitignore setup."""
    ...


def setup_githooks(ctx):  # type: (Context) -> None
    """Check githooks setup."""
    ...


@task(iterable=['name'])
def setup(
    ctx,
    update=False,
):  # type: (Context, bool) -> None
    """Clean project dependencies and build."""
    os.system('clear')
    print('This tool will assist with environment setup.', end='\n\n')

    # config = GlobalConfig(directory=ctx.dirs.config_dir)

    setup_gitconfig(ctx, update)
    setup_gitignore(ctx)
    setup_githooks(ctx)

    # if not os.path.exists(config.directory):
    #     os.mkdir(ctx.dirs.config_dir)

    # if update or not os.path.exists(config.filepath):
    #     config.dump()


tasks = Collection(setup)
