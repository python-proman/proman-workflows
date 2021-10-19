"""Provide templating for git hooks."""

import os

# import stat
from dataclasses import asdict

from invoke import Collection, Context, task

# from jinja2 import Environment, FileSystemLoader

from proman_workflows import git  # , filesystem, templates
from proman_workflows.config import HooksConfig


@task
def setup(ctx, name='pre-commit', update=False):
    # type: (Context, str, bool) -> None
    """Create git hook."""
    path = os.path.join(ctx.hooks_dir, name)
    if update or not os.path.exists(path):
        data = {
            'python_executable': ctx.python_path,
            'proman_namespace': 'proman.precommit',
            'proman_command': 'conventional_commits.update',
        }
        git.dump_config(
            ctx,
            data,
            template_name='invoke_hooks',
            dest=path,
            executable=True,
            update=update,
        )


# @task
# def index(ctx):  # type: (Context) -> None
#     """List git hooks."""
#     print('list contents')


@task
def remove(ctx, name='pre-commit'):  # type: (Context, str) -> None
    """Remove git hook."""
    path = os.path.join(ctx.hooks_dir, name)
    if os.path.exists(path):
        os.remove(path)


config = HooksConfig()
namespace = Collection()
namespace.configure(asdict(config))
namespace.add_task(setup)
namespace.add_task(remove)
