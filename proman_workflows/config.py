# copyright: (c) 2020 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
"""Provide CLI for git-tools."""

import os
import shutil
import sys
from dataclasses import dataclass, field

# from pprint import pprint
from typing import List

from compendium.loader import ConfigFile
from pygit2 import discover_repository

# from typing import Optional, Tuple
# from urllib.parse import urljoin, urlparse

VENV_PATH = os.getenv('VIRTUAL_ENV', None)
PATHS = [VENV_PATH] if VENV_PATH else []

# TODO check VCS for paths
python_path = sys.executable
repo_dir = discover_repository(os.getcwd())
project_dir = os.path.abspath(os.path.join(repo_dir, os.pardir))
specfiles = ['pyproject.toml', 'setup.cfg']

if shutil.which('podman'):
    container_runtime = 'podman'
elif shutil.which('docker'):
    container_runtime = 'docker'

templates_dir: str = os.path.join(os.path.dirname(__file__), 'templates')

# Paths
container_build_dir = os.getenv('CONTAINER_BUILD_DIR', '.')
working_dir = project_dir


@dataclass
class Plugin:
    """Provide proman_workflows plugin."""

    name: str
    driver_name: str
    driver_namespace: str


@dataclass
class ProjectDirs:
    """Project package."""

    python_path: str = sys.executable
    repo_dir: str = discover_repository(os.getcwd())
    base_dir: str = os.path.abspath(os.path.join(repo_dir, os.pardir))
    hooks_dir: str = field(init=False)
    templates_dir: str = field(init=False)
    container_build_dir: str = field(init=False)
    specfiles: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize project settings."""
        if not self.specfiles:
            self.specfiles = ['pyproject.toml', 'setup.cfg']
        if not self.hooks_dir:
            self.hooks_dir = os.path.join(self.repo_dir, 'hooks')
        if not self.templates_dir:
            self.templates_dir = os.path.join(self.base_dir, 'templates')
        if not self.container_build_dir:
            self.container_build_dir = self.base_dir


@dataclass
class GlobalConfig(ConfigFile):
    """Configuration for project management."""

    name: str
    writable: bool = True
    directory: str = field(init=False)
    filepath: str = field(init=False)

    def __post_init__(self) -> None:
        """Initialize settings from configuration."""
        self.directory = os.path.join(
            os.path.expanduser('~'), '.config', self.name
        )
        self.filepath = os.path.join(self.directory, 'proman.toml')
        super().__init__(
            self.filepath,
            writable=self.writable,
            separator='.',
        )
        if os.path.exists(self.filepath) and os.path.isfile(self.filepath):
            self.load()
        elif not os.path.exists(self.directory):
            os.makedirs(self.directory)
            self.dump()


# @dataclass
# class Credentials:
#     """Manage credentials."""
#
#     username: Optional[str] = None
#     password: Optional[str] = field(default=None, repr=False)
#     interactive: bool = True
#
#     def __post_init__(self) -> None:
#         """Initialize GPG settings."""
#         if self.interactive:
#             if not self.username:
#                 self.username = pyip.inputStr(
#                     prompt='Enter username: ',
#                     limit=255,
#                 )
#             if not self.password:
#                 self.password = pyip.inputPassword(
#                     prompt='Enter password: ',
#                     limit=255,
#                 )


@dataclass
class GPGConfig:
    """Manage GPG keys."""

    # commit_signing_key: str
    # package_signing_key: str
    home_dir: str = os.path.join(os.path.expanduser('~'), '.gnupg')


@dataclass
class DocsConfig:
    """Manage documentation configuration."""

    working_dir: str = os.getenv('DOCS_DIR', project_dir)


@dataclass
class WebConfig(ProjectDirs):
    """Manage web configuration."""

    environment = os.getenv('FLASK_ENV', 'development')
    webapp_dir: str = field(init=False)
    static_dir: str = field(init=False)

    def __post_init__(self) -> None:
        """Initialize settings."""
        if not self.webapp_dir:
            self.webapp_dir: str = os.path.join(self.base_dir, 'ui')
        if not self.static_dir:
            self.static_dir: str = os.path.join(self.webapp_dir, 'static')


@dataclass
class ContainerConfig:
    """Manage container configuration."""

    runtime: str

    def __post_init__(self) -> None:
        """Initialize container config."""
        if self.runtime:
            if shutil.which('podman'):
                self.runtime = 'podman'
            elif shutil.which('docker'):
                self.runtime = 'docker'
