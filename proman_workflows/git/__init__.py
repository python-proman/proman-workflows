'''Provide git capabilities.'''

from proman_workflows import repo
from proman_workflows.git.hooks import Hooks


def get_hooks_controller(
    hooks_dir: str = repo.hooks_dir, template: str = 'invoke_hooks'
) -> Hooks:
    return Hooks(hooks_dir, template)
