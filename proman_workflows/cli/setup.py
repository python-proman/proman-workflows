'''Provide setup capability.'''

from proman_workflows import repo


def commit_message(path: str = 'proman_workflows/templates/gitmessage.j2'):
    repo.config_writer().set_value("commit", "template", path).release()
