"""Provide templating for git hooks."""

import os
import stat
import sys
from dataclasses import asdict

from invoke import Collection, Context, task
from jinja2 import Environment, FileSystemLoader

from proman_workflows.config import HooksConfig


@task
def setup(ctx, name='pre-commit', update=False):
    # type: (Context, str, bool) -> None
    """Create git hook."""
    path = os.path.join(ctx.hooks_dir, name)
    if not os.path.exists(path) or update:
        file_system_loader = FileSystemLoader(ctx.templates_dir)
        env = Environment(loader=file_system_loader, autoescape=True)
        template = env.get_template(ctx.template)

        content = template.render(
            python_executable=sys.executable,
            proman_namespace='proman.precommit',
            proman_command='conventional_commits.update',
        )

        with open(path, 'w+') as f:
            f.write(content)

        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)


# @task
# def index(ctx):  # type: (Context) -> None
#     """List git setup git hooks."""
#     print('list contents')


@task
def remove(ctx, name='pre-commit'):  # type: (Context, str) -> None
    """Remove git hook."""
    path = os.path.join(ctx.hooks_dir, name)
    if os.path.exists(path):
        os.remove(path)


config = HooksConfig()
namespace = Collection(setup, remove)
namespace.configure(asdict(config))
