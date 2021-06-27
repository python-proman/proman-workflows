# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Parse Git commit messages.'''

# import logging
import os
import re
from copy import deepcopy
from string import Template
from typing import Any

from packaging.version import Version
# from transitions import Machine

from proman_workflows import exception
from proman_workflows.config import Config
from proman_workflows.parser import CommitMessageParser
from proman_workflows.vcs import GitRepo
from proman_workflows.version import PythonVersion

# TODO: version comparison against previous version
# has API spec been modified?
# has Python version changed?
# has requirements versions changed?


# TODO determine relation with state and git hooks
class ReleaseController(CommitMessageParser):
    def __init__(
        self,
        config: Config,
        workflow: GitRepo,
        *args: Any,
        **kwargs: Any
    ) -> None:
        '''Initialize commit message action object.'''
        self.config = config
        if self.config.retrieve('/tool/proman'):
            if 'version' in self.config['tool']['proman']['release']:
                version = config.retrieve('/tool/proman/release/version')
            else:
                version = config.retrieve('/tool/proman/version')
        elif self.config.retrieve('/tool/poetry'):
            version = config.retrieve('/tool/poetry/version')
        elif self.config.retrieve('/metadata'):
            version = config.retrieve('/metadata/version')
        self.version = PythonVersion(version)
        self.workflow = workflow

        super().__init__(*args, **kwargs)
        ref = self.workflow.repo.refs[
            str(self.workflow.repo.active_branch)
        ].commit
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
            file_contents = pattern.sub(new_version, file_contents)
            # TODO: error if pattern not found in contents
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
        self.workflow.commit(
            filepaths=tuple(f['filepath'] for f in filepaths),
            message=f"ci(version): apply {new_version} modifications"
        )

    def bump_version(self) -> str:
        '''Update the version of the application.'''
        # states = ['dev', 'alpha', 'beta', 'rc', 'final', 'post']
        version = deepcopy(self.version)
        new_version = None

        if self.title['break'] or self.footer['breaking_change']:
            new_version = self.version.bump_major()
        elif 'type' in self.title:
            if self.title['type'] == 'feat':
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

        if not self.workflow.repo.is_dirty():
            if new_version:
                self.update_configs(version=version, new_version=new_version)
            else:
                raise exception.PromanWorkflowException(
                    'no new version available'
                )
        else:
            raise exception.PromanWorkflowException(
                'git repository is not clean'
            )
        return str(version)
