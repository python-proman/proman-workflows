'''Provide templating for git hooks.'''

import config
import os
import sys
from typing import Any

from jinja2 import Environment, FileSystemLoader  # type: ignore


class GitHooks:
    def __init__(self, hooks_dir: str, template: str = 'invoke_hooks') -> None:
        '''Initialize git hooks object.'''
        self.hooks_dir = hooks_dir
        self.template = os.path.join(config.hooks_dir, template)

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
            )

            with open(path, 'w+') as f:
                f.write(content)
            os.chmod(path, 0o775)

    def remove(self, name: str = 'pre-commit') -> None:
        '''Remove git hook.'''
        path = os.path.join(self.hooks_dir, name)
        if os.path.exists(path):
            os.remove(path)
