# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for git-tools.'''

import git
import os
from configparser import ConfigParser

git_repo = git.Repo('.git', search_parent_directories=True)
git_root_path = git_repo.git.rev_parse('--show-toplevel')
git_hooks_path = os.path.join(git_root_path, '.git', 'hooks')
config_path = os.path.join(git_root_path, '.git-tools')

class Config:
    '''Provide settings for git-tools.'''

    def __init__(self, config_path):
        '''Initialize git-tools configuration.'''
        self.__settings = ConfigParser()

        if os.path.isfile(config_path):
            self.__settings.read(config_path)
        else:
            print('no configuration found')
