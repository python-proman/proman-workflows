# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for git-tools.'''

from dataclasses import dataclass
import os
# from pprint import pprint
from typing import Optional
from urllib.parse import urljoin, urlparse

from compendium.loader import ConfigFile
from git.config import GitConfigParser

INDEX_URL = urlparse('https://pypi.org')
VENV_PATH = os.getenv('VIRTUAL_ENV', None)
PATHS = [VENV_PATH] if VENV_PATH else []

# TODO check VCS for paths
base_dir = os.getcwd()
filenames = ['pyproject.toml', 'setup.cfg']
# pyproject_path = os.path.join(base_dir, 'pyproject.toml')
# lock_path = os.path.join(base_dir, 'proman-lock.json')
pypackages_dir = os.path.join(base_dir, '__pypackages__')

GIT_HOOKS = {
    'applypatch-msg',
    'pre-applypatch',
    'post-applypatch',
    'pre-commit',
    'pre-merge-commit',
    'prepare-commit-msg',
    'post-commit',
    'pre-rebase',
    'post-checkout',
    'post-merge',
    'pre-push',
    'pre-recieve',
    'update',
    'post-recieve',
    'post-update',
    'reference-transaction',
    'push-to-checkout',
    'pre-auto-gc',
    'post-rewrite',
    'rebase',
    'sendemail-validate',
    'fsmonitor-watchman',
    'p4-changelist',
    'p4-prepare-changelist',
    'p4-post-changelist',
    'p4-pre-submit',
    'post-index-change'
}

task_engine: str = 'invoke'
templates_dir: str = os.path.join(os.path.dirname(__file__), 'templates')

grammar: str = os.path.join(
    os.path.dirname(__file__), 'grammars', 'conventional_commits.lark'
)


@dataclass
class GitConfig:
    '''Manage git config.'''

    system_config: str = os.path.join(os.sep, 'etc', 'gitconfig')
    global_config: str = os.path.join(os.path.expanduser('~'), '.gitconfig')

    def __post_init__(self) -> None:
        self.load()

    def load(self) -> None:
        '''Load git configuration.'''
        with GitConfigParser(self.global_config, read_only=True) as cfg:
            cfg.read()
            if not cfg.has_section('commit'):
                cfg.add_section('commit')
            # pprint(cfg.__dict__)  # ._sections)

    def save(self) -> None:
        '''Save git configuration.'''
        with GitConfigParser(self.global_config, read_only=False) as cfg:
            if not cfg.has_section('commit'):
                cfg.add_section('commit')
            cfg.write()


@dataclass
class Config(ConfigFile):
    '''Manage settings from configuration file.'''

    filepath: str
    index_url: str = urljoin(INDEX_URL.geturl(), 'simple')
    python_versions: tuple = ()
    digest_algorithm: str = 'sha256'
    include_prereleases: bool = False
    lookup_memory: Optional[str] = None
    writable: bool = True

    def __post_init__(self) -> None:
        '''Initialize settings from configuration.'''
        super().__init__(self.filepath)
        if os.path.isfile(self.filepath):
            self.load()
