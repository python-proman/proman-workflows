"""Provide git management capabilities."""

import os
from typing import TYPE_CHECKING, Any, Dict, Optional

from invoke import Collection, task
from pygit2 import Config, Repository

# import pyinputplus as pyip

from .. import filesystem, templates

if TYPE_CHECKING:
    from invoke import Context


@task
def repo(ctx):  # type: (Context) -> Repository
    """Set git as SCM."""
    return Repository(ctx.repo_dir)


@task
def dump_config(
    ctx, data, template_name, dest, executable=False, update=False
):  # type: (Context, Dict[str, Any], str, str, bool, bool) -> None
    """Create git hook."""
    print('dest', dest)
    if update or not os.path.exists(dest):
        content = templates.render(ctx, data, template_name=template_name)
        filesystem.write(
            ctx,
            content=content,
            dest=dest,
            executable=executable,
            update=update,
        )


@task
def get_config(ctx):  # type: (Context) -> None
    """Retrieve git configuration."""
    scm = repo(ctx)
    for entry in scm.config:
        if entry.name == 'core':
            print(entry.value)
        else:
            print(entry.name, entry.value)


def config_to_dict(config: Config) -> Dict[str, Any]:
    """Convert gitconfig to dictionary."""
    sections: Dict[str, Any] = {}
    for entry in config:
        section, name = entry.name.split('.', 1)
        if section not in sections:
            sections[section] = {}
        sections[section][name] = entry.value
    return {'sections': sections}


@task
def config(
    ctx, scope=None
):  # type: (Context, Optional[str]) -> Dict[str, Any]
    """Get git config as dictionary."""
    vcs = repo(ctx)
    if scope == 'system':
        config = vcs.config.get_system_config()
    elif scope == 'global':
        config = vcs.config.get_global_config()
    elif scope == 'xdg':
        config = vcs.config.get_xdg_config()
    else:
        config = Config(os.path.join(ctx.repo_dir, 'config'))
    return config_to_dict(config)


@task
def setup(
    ctx, scope=None, update=False
):  # type: (Context, Optional[str], bool) -> None
    """Set VCS configuration."""
    data = config(ctx, scope)

    # if 'user.name' not in config:
    #     username = pyip.inputStr(
    #         prompt='GIT: Enter full name: ',
    #         limit=255,
    #     )
    #     config.set_multivar('user.name', regex='^.*$', value=username)
    #     print('user.name', config.get_multivar('user.name'))
    # if 'user.email' not in config:
    #     email = pyip.inputEmail(
    #         prompt='GIT: Enter email: ',
    #         limit=255,
    #     )
    #     config.set_multivar('user.email', regex='^.*$', value=email)
    #     print('user.email', config.get_multivar('user.email'))

    dump_config(
        ctx,
        data,
        template_name='gitconfig',
        dest=os.path.join(ctx.repo_dir, 'check'),
        update=update,
    )


namespace = Collection(get_config, setup)
