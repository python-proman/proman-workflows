# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Parse Git commit messages.'''

# import logging
from typing import Any

from transitions import Machine

from proman_workflows.config import Config
from proman_workflows.parser import CommitMessageParser


class GitFlow(CommitMessageParser):
    '''Provide commit message state engine.'''

    main_branches = ['master', 'develop']
    support_branches = ['feature', 'release', 'hotfix']
    states = ['development', 'release', 'maintenance', 'stable']
    release_types = ['alpha', 'beta', 'rc', 'post', 'final']

    def __init__(
        self,
        name: str,
        config: Config,
        *args: Any,
        **kwargs: Any
    ) -> None:
        '''Initialize commit message base class.

        Reconcile current version with commit message type.
        '''
        self.name = name
        self.config = config

        transitions = [
            {
                'trigger': 'create_feature',
                'source': 'stable',
                'dest': 'development'
            }, {
                'trigger': 'add_feature',
                'source': 'development',
                'dest': 'release'
            }, {
                'trigger': 'create_hotfix',
                'source': ['stable', 'release'],
                'dest': 'maintenance',
            }, {
                'trigger': 'add_hotfix',
                'source': 'maintenance',
                'dest': ['development', 'release', 'stable'],
            }, {
                'trigger': 'create_release',
                'source': 'development',
                'dest': 'release'
            }, {
                'trigger': 'finish_release',
                'source': 'release',
                'dest': 'stable'
            }
        ]
        self.machine = Machine(
            self,
            states=GitFlow.states,
            transitions=transitions,
            initial='development'
        )

    @property
    def current_version(self) -> str:
        return self.config.retrieve('/tool/proman/version')

    def version(self) -> None:
        print(self.title)
