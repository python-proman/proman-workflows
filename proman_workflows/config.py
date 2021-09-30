# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
"""Provide CLI for git-tools."""

import os
import shutil
import sys
from dataclasses import dataclass, field

# from pprint import pprint
from pygit2 import discover_repository
from typing import Optional, Tuple
from urllib.parse import urljoin, urlparse

from compendium.loader import ConfigFile

INDEX_URL = urlparse('https://pypi.org')
VENV_PATH = os.getenv('VIRTUAL_ENV', None)
PATHS = [VENV_PATH] if VENV_PATH else []

# TODO check VCS for paths
python_path = sys.executable
repo_dir = discover_repository(os.getcwd())
basedir = os.path.abspath(os.path.join(repo_dir, os.pardir))
specfiles = ['pyproject.toml', 'setup.cfg']

if shutil.which('podman'):
    container_runtime = 'podman'
elif shutil.which('docker'):
    container_runtime = 'docker'

templates_dir: str = os.path.join(os.path.dirname(__file__), 'templates')

# Paths
project_path = os.getenv('PROJECT_PATH', '.')
working_dir = basedir

# Settings
environment = os.getenv('FLASK_ENV', 'development')


@dataclass
class GPGConfig:
    """Manage GPG keys."""

    gpg_home: str = os.path.join(os.path.expanduser('~'), '.gnupg')


@dataclass
class HooksConfig:
    """Manage hooks config."""

    hooks_dir: str = os.path.join(basedir, '.git', 'hooks')
    hooks: Tuple[str, ...] = (
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
        'post-index-change',
    )


@dataclass
class Config(ConfigFile):
    """Manage settings from configuration file."""

    filepath: str
    index_url: str = urljoin(INDEX_URL.geturl(), 'simple')
    python_versions: tuple = ()
    digest_algorithm: str = 'sha256'
    include_prereleases: bool = False
    lookup_memory: Optional[str] = None
    writable: bool = True

    def __post_init__(self) -> None:
        """Initialize settings from configuration."""
        super().__init__(self.filepath)
        if os.path.isfile(self.filepath):
            self.load()


@dataclass
class WebConfig:
    """Manage web configuration."""

    webapp_dir: str = basedir
    static_dir: str = 'static'
    webui_dir: str = field(init=False)

    def __post_init__(self) -> None:
        """Initialize settings."""
        self.webui_dir: str = os.path.join(self.static_dir, 'webui')


@dataclass
class DocsConfig:
    """Manage documentation configuration."""

    working_dir: str = os.getenv('DOCS_DIR', basedir)
