# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Parse Git commit messages.'''

# import logging
import re
from typing import Any

from git import Repo
from transitions import Machine

from proman_workflows.vcs import Git


class VCSWorkflow:
    ...


class GitFlow(Git, VCSWorkflow):
    '''Provide branching state engine.'''

    main_branches = ['develop', 'master']
    support_branches = ['feature', 'hotfix', 'release']
    states = support_branches + main_branches
    pattern = r'''
        ^(?P<kind>feat|fix|rc)
        (?:
            [/_-]?
            (?P<name>[A-Za-z]\w+)
        )
        (?:
            [_-]?
            (?P<id>\d+)
        )?$
    '''

    def __init__(
        self,
        repo: Repo,
        *args: Any,
        **kwargs: Any
    ) -> None:
        '''Initialize commit message base class.

        Reconcile current version with commit message type.
        '''
        super().__init__(repo)
        self.name = kwargs.get('branch', str(repo.active_branch))

        transitions = [
            {
                'trigger': 'setup_develop',
                'source': 'master',
                'dest': 'develop',
                'before': 'check_branch',
                'after': 'update_branch',
            }, {
                'trigger': 'feature_start',
                'source': 'develop',
                'dest': 'feature',
            }, {
                'trigger': 'feature_finish',
                'source': 'feature',
                'dest': 'develop',
                'before': 'refresh_main',
                'after': 'finalize_feature',
            }, {
                'trigger': 'hotfix_start',
                'source': 'master',
                'dest': 'hotfix',
            }, {
                'trigger': 'hotfix_finish',
                'source': 'hotfix',
                'dest': 'master',
                'before': 'refresh_main',
                'after': 'finalize_hotfix'
            }, {
                'trigger': 'release_start',
                'source': 'develop',
                'dest': 'release',
            }, {
                'trigger': 'release_finish',
                'source': 'release',
                'dest': 'master',
                'before': 'refresh_main',
                'after': 'finalize_release',
            }
        ]
        self.machine = Machine(
            self,
            states=GitFlow.states,
            transitions=transitions,
            initial=self.get_initial_state()
        )

    def refresh_main(self) -> None:
        print('pulling sources')

    def finalize_feature(self) -> None:
        print('merge feature into develop')

    def finalize_hotfix(self) -> None:
        print('merge hotfix to develop/master')

    def finalize_release(self) -> None:
        print('pushing release to develop/master')

    def get_initial_state(self) -> str:
        if self.name == 'develop' or self.name == 'master':
            return self.name
        else:
            pattern = re.compile(GitFlow.pattern, re.VERBOSE | re.IGNORECASE)
            if pattern:
                result = re.search(pattern, self.name)
                if result:
                    if result['kind'] == 'feat':
                        return 'feature'
                    elif result['kind'] == 'fix':
                        return 'hotfix'
                    elif result['kind'] == 'rc':
                        return 'release'
        return 'master'
