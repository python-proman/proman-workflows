"""Check git repo configuration."""

import os
from dataclasses import dataclass

from pygit2 import Repository


@dataclass
class Config:
    """Provide git configuration."""

    pass


repo = Repository(os.path.join('.'))
print(repo.config.__dict__)
for entry in repo.config:
    if entry.name == 'core':
        print(entry.value)
    else:
        print(entry.name, entry.value)

global_config = repo.config.get_global_config()
for entry in global_config:
    print(entry.name, entry.value)
