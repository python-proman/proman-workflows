# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git submodules.'''

from typing import Optional

# from git.objects.submodule.base import Submodule
# from git.objects.submodule.root import (
#     RootModule,
#     RootUpdateProgress
# )
# from git.repo.fun import (
#     find_submodule_git_dir,
#     touch
# )

from invoke import task

from proman_workflows import repo

base_dir = 'modules'

post_commit = '''#!/bin/bash
exec git submodule update
'''


# def setup() -> None:
#     '''Do setup for post checkout hooks.'''
#     path = os.path.join(os.getcwd(), '.git', 'hooks', 'post-checkout')
#     with open(path, 'w') as f:
#         f.write(post_commit)


@task
def index() -> None:
    '''List submodules with project.'''
    for sm in repo.submodules:
        print(sm)


@task
def view(name: Optional[str] = None) -> None:
    '''View project info.'''
    if name:
        sm = repo.submodule(name)
        print(sm.children())
    else:
        print('No module name provided')


@task
def add(
    module: Optional[str] = None,
    url: Optional[str] = None,
    branch: str = 'master',
    path: Optional[str] = None
) -> None:
    '''Add submodule to project.'''
    repo.create_submodule(module, path, url=url, branch=branch)
    repo.index.commit(f'Added {module} submodule')


@task
def update(name: Optional[str] = None) -> None:
    '''Update submodule within project.'''
    if name:
        sm = repo.submodule(name)
        sm.update(recursive=True, init=True)
    else:
        repo.submodule_update(recursive=False)


@task
def remove(
    name: Optional[str] = None,
    module: bool = True,
    force: bool = True,
    configuration: bool = True
) -> None:
    '''Remove submodule from repository.

    Parameters
    ----------
    name:
        Name of submodule to be removed
    module:
        Remove module from repsitory
    force:
        Force removal even with changes
    configuration:
        Remove module from configuration

    '''
    sm = repo.submodule(name)
    sm.remove(module=module, force=force, configuration=configuration)
