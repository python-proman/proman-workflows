# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Parse Git commit messages.'''

# import logging
import os
from typing import Any, Optional, Tuple

from git import Repo
# from transitions import Machine

# TODO: version comparison against previous version
# has API spec been modified?
# has Python version changed?
# has requirements versions changed?


class VCSWorkflow:
    ...


class GitRepo:
    def __init__(self, repo: Repo) -> None:
        '''Initialize git object.'''
        self.repo = repo
        self.branch = 'master'

    def init(self, path: str) -> None:
        '''Initialize a Git repository.'''
        if not os.path.exists(os.path.join(path, '.git')):
            Repo.init(path)
        else:
            print('Repository already initialized.')

    def clone(
        self,
        repo: Repo,
        path: str = '.',
        branch: str = 'master',
    ) -> None:
        '''Clone Git repository.'''
        if not os.path.exists(path):
            Repo.clone_from(repo, path, branch=branch)
        # else:
        #     raise exceptions.VCSException('clone already exists')

    def add_remote(
        self,
        remote: Repo,
        name: str = 'origin',
        branch: str = 'master',
    ) -> None:
        '''Add Git remote repository URL.'''
        if next(iter(self.repo.remotes), None) is None:
            self.repo.create_remote(name, url=remote)
        else:
            for remote in self.repo.remotes:
                if name == remote.name:
                    remote.set_url(self.repo)
                else:
                    self.repo.create_remote(name, url=remote)

    def checkout(self, name: str) -> None:
        '''Checkout Git branch.'''
        new_branch = self.repo.create_head(name)
        self.repo.head.reference = new_branch

    def push(
        self,
        remote: str = 'origin',
        branch: str = 'master',
    ) -> None:
        '''Push Git commits to repository.'''
        origin = self.repo.remotes[remote]
        origin.fetch()
        origin.push(branch or self.branch)

    def pull(self) -> None:
        ...

    def merge(self) -> None:
        ...

    def commit(
        self,
        basedir: str = os.getcwd(),
        filepaths: Tuple[Any, ...] = (),
        message: str = 'initial commit',
    ) -> None:
        '''Commit changes in a Git repository.'''
        if filepaths == ():
            filepaths = (os.path.join(basedir, '*'),)
        for filepath in filepaths:
            self.repo.index.add(os.path.join(basedir, filepath))
        self.repo.index.commit(message)

    # def commit(
    #     self,
    #     items=[],
    #     path=config.working_dir,
    #     message='initial commit'
    # ):
    #     '''Commit changes in a Git repository.'''
    #     if items == []:
    #         items = os.path.join(path, '*')
    #     self.repo.index.add(items)
    #     self.repo.index.commit(message)

    def tag(
        self,
        path: str,
        ref: str = 'HEAD',
        message: Optional[str] = None,
        force: bool = False,
        **kwargs: Any
    ) -> None:
        '''Tag commit message.'''
        self.repo.create_tag(
            path=path, ref=ref, message=message, force=force, **kwargs
        )
