# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for git-tools.'''

from dataclasses import dataclass, field
import os
# from pprint import pprint

import git
from git.config import GitConfigParser

__hooks__ = {
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
    'proman_workflows', 'grammars', 'conventional_commits.lark'
)

git_repo: str = git.Repo('.git', search_parent_directories=True)
git_repo_dir: str = git_repo.git.rev_parse('--show-toplevel')

git_dir: str = os.path.join(git_repo_dir, '.git')
git_tools_dir: str = os.path.join(git_repo_dir, '.proman-source')
git_hooks_dir: str = os.path.join(git_dir, 'hooks')

git_system_config: str = os.path.join(os.sep, 'etc', 'gitconfig')
git_global_config: str = os.path.join(os.path.expanduser('~'), '.gitconfig')
git_config: str = os.path.join(git_dir, 'config')


@dataclass
class GitDirs:
    '''Provide settings for git-tools.'''

    repo: str = git.Repo('.git', search_parent_directories=True)
    repo_dir: str = repo.git.rev_parse('--show-toplevel')

    git_dir: str = field(init=False)
    hooks_dir: str = field(init=False)
    tools_dir: str = field(init=False)

    system_config: str = os.path.join(os.sep, 'etc', 'gitconfig')
    global_config: str = os.path.join(os.path.expanduser('~'), '.gitconfig')
    config: str = field(init=False)

    def __post_init__(self) -> None:
        '''Initialize git-tools configuration.'''
        self.tools_dir = os.path.join(self.repo_dir, '.git-tools')
        self.git_dir = os.path.join(self.repo_dir, '.git')
        self.hooks_dir = os.path.join(self.git_dir, 'hooks')
        self.config = os.path.join(self.git_dir, 'config')


# @dataclass
# class GitConfig(GitDirs):
#     '''Manage git config.'''
#
#     def load(self) -> None:
#         '''Load git configuration.'''
#         with GitConfigParser(self.global_config, read_only=True) as cfg:
#             cfg.read()
#             if not cfg.has_section('commit'):
#                 cfg.add_section('commit')
#             # pprint(cfg.__dict__)  # ._sections)
#
#     def save(self) -> None:
#         '''Save git configuration.'''
#         with GitConfigParser(self.global_config, read_only=False) as cfg:
#             if not cfg.has_section('commit'):
#                 cfg.add_section('commit')
#             cfg.write()


class GitConfig(GitConfigParser):
    pass
