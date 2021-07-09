'''Provide setup capability.'''

from typing import Optional
from proman_workflows.git import hooks
from invoke import Collection, Context, task

from proman_workflows import repo


@task
def update(ctx, package=None, force=False):
    # type: (Context, Optional[str], bool) -> None
    '''Update example.'''
    print('yeppers')


@task
def commit_message(ctx, path='proman_workflows/templates/gitmessage.j2'):
    # type: (Context, str) -> None
    '''Proide conventional commit directions.'''
    repo.config_writer().set_value("commit", "template", path).release()


tasks = Collection().from_module(hooks)
