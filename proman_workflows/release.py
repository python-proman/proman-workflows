# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Parse Git commit messages.'''

# import logging
import os
import re
from copy import deepcopy
from string import Template
from typing import Any, Optional, Tuple

from packaging.version import (
    _cmpkey,
    # _parse_local_version,
    _Version,
    Version,
)
from transitions import Machine

from proman_workflows import repo, source_tree
from proman_workflows.config import Config
from proman_workflows.parser import CommitMessageParser


class PythonVersion(Version):
    '''Provide PEP440 compliant versioning.'''
    # development = ['development']
    # release = ['alpha', 'beta', 'candidate']
    # final = ['final']
    # post = ['post']
    # states = development + release + final + post
    # states = ['dev', 'alpha', 'beta', 'candidate', 'final', 'post']

    def __init__(self, version: str, **kwargs: Any) -> None:
        '''Initialize version object.'''
        # self.kind = kwargs.pop('version_system', 'semver')
        super().__init__(version=version)

        # transitions = [
        #     {
        #         'trigger': 'start_development',
        #         'source': ['final', 'post'],
        #         'dest': 'development'
        #     }, {
        #         'trigger': 'create_release',
        #         'source': 'development',
        #         'dest': PythonVersion.release
        #     }, {
        #         'trigger': 'finalize_release',
        #         'source': PythonVersion.release,
        #         'dest': 'final'
        #     }, {
        #         'trigger': 'post_release',
        #         'source': 'final',
        #         'dest': 'post'
        #     }
        # ]

        # self.machine = Machine(
        #     self,
        #     states=PythonVersion.states,
        #     transitions=transitions,
        #     initial=self.get_state()
        # )

    def get_state(self) -> str:
        '''Get the current state of package release.'''
        if self.is_devrelease:
            state = 'development'
        elif self.is_prerelease and self.pre:
            if self.pre[0] == 'a':
                state = 'alpha'
            elif self.pre[0] == 'b':
                state = 'beta'
            elif self.pre == 'rc':
                state = 'release'
            state = 'release'
        elif self.is_postrelease:
            state = 'post'
        else:
            state = 'final'
        return state

    def __update_version(
        self,
        epoch: Optional[int] = None,
        release: Optional[Tuple[Any, ...]] = None,
        pre: Optional[Tuple[str, int]] = None,
        post: Optional[Tuple[str, int]] = None,
        dev: Optional[Tuple[str, int]] = None,
        local: Optional[str] = None,
    ) -> None:
        '''Update the internal version state.'''
        if not (epoch or release):
            pre = pre or self.pre
            post = post or self.post
            dev = dev or self.dev
            local = local or self.local

        self._version = _Version(
            epoch=epoch or self.epoch,
            release=release or self.release,
            pre=pre,
            post=post,
            dev=dev,
            local=local,
        )

        self._key = _cmpkey(
            self._version.epoch,
            self._version.release,
            self._version.pre,
            self._version.post,
            self._version.dev,
            self._version.local,
        )

    def bump_epoch(self) -> 'PythonVersion':
        '''Update epoch releaes to next version number.'''
        self.__update_version(epoch=self.epoch + 1)
        return self

    def bump_major(self) -> 'PythonVersion':
        '''Update major release to next version number.'''
        self.__update_version(release=(self.major + 1, 0, 0))
        return self

    def bump_minor(self) -> 'PythonVersion':
        '''Update minor release to next version number.'''
        self.__update_version(release=(self.major, self.minor + 1, 0))
        return self

    def bump_micro(self) -> 'PythonVersion':
        '''Update micro release to next version number.'''
        self.__update_version(release=(self.major, self.minor, self.micro + 1))
        return self

    def bump_devrelease(self) -> 'PythonVersion':
        '''Update to the next development release version number.'''
        if self.dev:
            dev = (self.dev[0], self.dev[1] + 1)
        else:
            dev = ('dev', 0)
        self.__update_version(dev=dev)
        return self

    def bump_prerelease(self) -> 'PythonVersion':
        '''Update the prerelease version number.'''
        if self.pre:
            pre = (self.pre[0], self.pre[1] + 1)
        else:
            pre = ('a', 0)
        self.__update_version(pre=pre)
        return self

    def next_prerelease(self) -> 'PythonVersion':
        '''Update to next prerelease version type.'''
        if self.pre and self.is_prerelease:
            if self.pre[0] == 'a':
                pre = ('b', 0)
            elif self.pre[0] == 'b':
                pre = ('rc', 0)
        else:
            pre = ('a', 0)
        self.__update_version(pre=pre)
        return self

    def bump_postrelease(self) -> 'PythonVersion':
        '''Update the post release version number.'''
        if self.post:
            post = (self.post[0], self.post[1] + 1)
        else:
            post = ('post', 0)
        self.__update_version(post=post)
        return self

    # def bump_local(self) -> 'PythonVersion':
    #     self.__update_version(local=self.local + 1)
    #     return self


class GitFlow:
    '''Provide branching state engine.'''

    main_branches = ['master', 'develop']
    support_branches = ['feature', 'release', 'hotfix']
    states = ['development', 'release', 'maintenance', 'final']

    def __init__(
        self,
        name: str = repo.active_branch,
        *args: Any,
        **kwargs: Any
    ) -> None:
        '''Initialize commit message base class.

        Reconcile current version with commit message type.
        '''
        self.name = name

        transitions = [
            {
                'trigger': 'create_feature',
                'source': 'final',
                'dest': 'development'
            }, {
                'trigger': 'add_feature',
                'source': 'development',
                'dest': 'release'
            }, {
                'trigger': 'create_hotfix',
                'source': ['final', 'release'],
                'dest': 'maintenance',
            }, {
                'trigger': 'add_hotfix',
                'source': 'maintenance',
                'dest': ['development', 'release', 'final'],
            }, {
                'trigger': 'create_release',
                'source': 'development',
                'dest': 'release'
            }, {
                'trigger': 'finish_release',
                'source': 'release',
                'dest': 'final'
            }
        ]
        self.machine = Machine(
            self,
            states=GitFlow.states,
            transitions=transitions,
            initial='development'
        )

    def current_branch(self) -> str:
        return 'master'


# TODO determine relation with state and git hooks


class CommitMessageAction(CommitMessageParser):
    def __init__(
        self,
        config: Config = source_tree,
        branch: str = str(repo.active_branch),
        *args: Any,
        **kwargs: Any
    ) -> None:
        '''Initialize commit message action object.'''
        self.config = config
        self.version = PythonVersion(config.retrieve('/tool/proman/version'))

        super().__init__(*args, **kwargs)
        ref = repo.refs[branch].commit
        self.parse(ref.message)

    def __update_config(
        self,
        filepath: str,
        version: str,
        new_version: str
    ) -> None:
        '''Update config file with new file.'''
        # TODO: if file does not exist
        with open(filepath, 'r+') as f:
            file_contents = f.read()
            pattern = re.compile(re.escape(version), flags=0)
            # TODO: if pattern not found
            file_contents = pattern.sub(new_version, file_contents)
            f.seek(0)
            f.truncate()
            f.write(file_contents)

    def update_configs(self, version: Version, new_version: Version) -> None:
        '''Update version within config files.'''
        filepaths = self.config.retrieve('/tool/proman/release/files')
        for filepath in filepaths:
            self.__update_config(
                filepath=os.path.join(os.getcwd(), filepath['filepath']),
                version=(
                    Template(filepath['pattern'])
                    .substitute(version=str(version))
                ),
                new_version=(
                    Template(filepath['pattern'])
                    .substitute(version=new_version)
                )
            )

    def bump_version(self) -> str:
        '''Update the version of the application.'''
        # states = ['dev', 'alpha', 'beta', 'rc', 'final', 'post']
        version = deepcopy(self.version)
        if (
            ('break' in self.title and self.title['break'])
            or (
                'breaking_change' in self.footer
                and self.footer['breaking_change']
            )
        ):
            new_version = self.version.bump_major()
        elif self.title['type'] == 'feat':
            new_version = self.version.bump_minor()
        elif self.title['type'] == 'fix':
            new_version = self.version.bump_micro()
        # update release instance
        elif self.title['type'] == 'build':
            # build number
            ...
        elif self.title['type'] == 'ci':
            # build number
            ...
        elif self.title['type'] == 'chore':
            # build number
            ...
        elif self.title['type'] == 'docs':
            # build number
            ...
        elif self.title['type'] == 'perf':
            # build number
            # potential for breaking change
            ...
        elif self.title['type'] == 'refactor':
            # build number
            # potential for breaking change
            ...
        elif self.title['type'] == 'style':
            # build number
            ...
        elif self.title['type'] == 'test':
            # build number
            ...
        self.update_configs(version=version, new_version=new_version)
        return str(version)
