# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for git-tools.'''

import git
import os
from pprint import pprint
from git.config import GitConfigParser

git_repo: str = git.Repo('.git', search_parent_directories=True)
git_root_path: str = git_repo.git.rev_parse('--show-toplevel')
git_manage_path: str = os.path.join(git_root_path, '.git')
git_hooks_path: str = os.path.join(git_manage_path, 'hooks')
git_tools_path: str = os.path.join(git_root_path, '.git-tools')

git_cfg_sys_path: str = os.path.join(os.sep, 'etc', 'gitconfig')
git_cfg_home_path: str = os.path.join(os.path.expanduser('~'), '.gitconfig')
git_cfg_repo_path: str = os.path.join(git_manage_path, 'config')

grammar: str = os.path.join(
    'git_tools', 'grammars', 'conventional_commits.lark'
)


class Config:
    '''Provide settings for git-tools.'''

    def __init__(self, path: str = git_tools_path):
        '''Initialize git-tools configuration.'''
        with GitConfigParser(git_cfg_home_path, read_only=False) as cfg:
            cfg.read()
            if not cfg.has_section('commit'):
                cfg.add_section('commit')
            cfg.write()
            pprint(cfg.__dict__)  # ._sections)
