'''Provide setup capability.'''

import git

repo = git.Repo('.')


def commit_message(path: str = 'git_tools/templates/gitmessage.j2'):
    repo.config_writer().set_value("commit", "template", path).release()
