# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
'''Control Git submodules.'''

from typing import Optional

from invoke import Collection, Context, task

from proman_workflows import repo

# from git.objects.submodule.base import Submodule
# from git.objects.submodule.root import (
#     RootModule,
#     RootUpdateProgress
# )
# from git.repo.fun import (
#     find_submodule_git_dir,
#     touch
# )



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
def index(ctx):  # type: (Context) -> None
    '''List submodules with project.'''
    for sm in repo.submodules:
        print(sm)


@task
def view(ctx, name=None):  # type: (Context, Optional[str]) -> None
    '''View project info.'''
    if name:
        sm = repo.submodule(name)
        print(sm.children())
    else:
        print('No module name provided')


@task
def add(ctx, module=None, url=None, branch='master', path=None):
    # type: (Context, Optional[str], Optional[str], str, Optional[str]) -> None
    '''Add submodule to project.'''
    repo.create_submodule(module, path, url=url, branch=branch)
    repo.index.commit(f'Added {module} submodule')


@task
def update(ctx, name=None):  # type: (Context, Optional[str]) -> None
    '''Update submodule within project.'''
    if name:
        sm = repo.submodule(name)
        sm.update(recursive=True, init=True)
    else:
        repo.submodule_update(recursive=False)


@task
def remove(
    ctx, name=None, module=True, force=True, configuration=True
):  # type: (Context, Optional[str], bool, bool, bool) -> None
    '''Remove submodule from repository.

    Parameters
    ----------
    ctx:
        Invoke context
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


submodule_tasks = Collection(add, index, view, remove, update)
