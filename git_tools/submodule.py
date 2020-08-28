# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git submodules.'''
import os
from git import Repo

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
repo = Repo('.')

post_commit = '''#!/bin/bash
exec git submodule update
'''


def setup(ctx):
    '''Do setup for post checkout hooks.'''
    path = os.getcwd() + '/.git/hooks/post-checkout'
    with open(path, 'w') as f:
        f.write(post_commit)


def index(ctx):
    '''List submodules with project.'''
    for sm in repo.submodules:
        print(sm)


def view(ctx, name=None):
    '''View project info.'''
    if name:
        sm = repo.submodule(name)
        print(sm.children())
    else:
        print('No module name provided')


def add(ctx, module=None, url=None, branch='master', path=None):
    '''Add submodule to project.'''
    repo.create_submodule(module, path, url=url, branch=branch)
    repo.index.commit(f'Added {module} submodule')


def update(ctx, name=None):
    '''Update submodule within project.'''
    if name:
        sm = repo.submodule(name)
        sm.update(recursive=True, init=True)
    else:
        repo.submodule_update(recursive=False)


def remove(ctx, name=None, module=True, force=True, configuration=True):
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
