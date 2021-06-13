# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git hooks.'''

import os
import sys

from jinja2 import Template

from proman_workflows import config

__hooks_template__ = """\
#!{{ python_executable }}
# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test git hooks pipeline.'''

from git import Repo
from pypyr import log, pipelinerunner

git_repo = Repo('.git', search_parent_directories=True)
git_root_path = git_repo.git.rev_parse('--show-toplevel')

log.logger.set_root_logger(
    log_level={{ log_level }},
    log_path={% if log_path %}'{{ log_path }}'{% else %}None{% endif %}
)

pipelinerunner.main(
    pipeline_name='.git-hooks',
    pipeline_context_input='{{ pipeline_context_input }}',
    working_dir=git_root_path,
    groups=[
        {%- for group in groups -%}
            '{{ group }}'{% if not loop.last %}, {% endif %}
        {%- endfor -%}
    ],
    success_group='{{ success_group }}',
    failure_group='{{ failure_group }}',
)
"""

__template__ = """\
from invoke import Collection, Program
from git import Repo
from git_tools import hooks

repo = Repo('.git', search_parent_directories=True)
path = repo.git.rev_parse('--show-toplevel')

hook = Program(namespace=Collection.from_module(hooks), version='0.1.0')
hook.run
"""


def setup(name: str = 'pre-commit', update: bool = False):
    '''Do setup for post checkout hooks.'''
    path = os.path.join(config.git_hooks_path, name)
    if not os.path.exists(path) or update:
        template = Template(__hooks_template__)
        content = template.render(
            python_executable=sys.executable,
            pipeline_context_input='arb context input',
            working_dir=config.git_root_path,
            groups=[name],
            success_group=f"{name}-success-group",
            failure_group=f"{name}-failure-group",
            log_level=25,
            log_path=None
        )

        with open(path, 'w+') as f:
            f.write(content)
        os.chmod(path, 0o775)


def remove(name: str = 'pre-commit'):
    '''Remove submodule from repository.

    Parameters
    ----------
    name:
        Name of submodule to be removed

    '''
    path = os.path.join(config.git_hooks_path, name)
    if os.path.exists(path):
        os.remove(path)
