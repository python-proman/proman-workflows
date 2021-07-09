# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git hooks.'''

import os
import sys
from typing import Any

from jinja2 import Environment, FileSystemLoader

from proman_workflows import config, repo


class Hooks:
    def __init__(self, hooks_dir: str, template: str = 'invoke_hooks') -> None:
        '''Initialize git hooks object.'''
        self.hooks_dir = hooks_dir
        self.template = f"{template}.j2"

    def setup(
        self,
        name: str = 'pre-commit',
        update: bool = False,
        **kwargs: Any,
    ) -> None:
        '''Do setup for post checkout hooks.'''
        path = os.path.join(self.hooks_dir, name)
        if not os.path.exists(path) or update:
            file_system_loader = FileSystemLoader(config.templates_dir)
            env = Environment(loader=file_system_loader)
            template = env.get_template(self.template)

            content = template.render(
                python_executable=sys.executable,
                # other variables
            )

            with open(path, 'w+') as f:
                f.write(content)
            os.chmod(path, 0o775)

    def remove(self, name: str = 'pre-commit') -> None:
        '''Remove git hook.'''
        path = os.path.join(self.hooks_dir, name)
        if os.path.exists(path):
            os.remove(path)


def setup(name: str = 'pre-commit', update: bool = False) -> None:
    '''Do setup for post checkout hooks.'''
    hooks = Hooks(repo.hooks_dir, 'invoke_hooks')
    hooks.setup(name, update)


def remove(name: str = 'pre-commit') -> None:
    '''Remove submodule from repository.

    Parameters
    ----------
    name:
        Name of submodule to be removed

    '''
    hooks = Hooks(repo.hooks_dir, 'invoke_hooks')
    hooks.remove(name)
