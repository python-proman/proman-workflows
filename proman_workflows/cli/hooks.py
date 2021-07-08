# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git hooks.'''

from proman_workflows.git import get_hooks_controller

hooks = get_hooks_controller()


def setup(name: str = 'pre-commit', update: bool = False) -> None:
    '''Do setup for post checkout hooks.'''
    hooks.setup(name, update)


def remove(name: str = 'pre-commit') -> None:
    '''Remove submodule from repository.

    Parameters
    ----------
    name:
        Name of submodule to be removed

    '''
    hooks.remove(name)
