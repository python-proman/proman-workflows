# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Convenience tools to manage Git projects with Python.'''

import logging
import os

from git import Repo

from proman_workflows.config import Config
from proman_workflows.parser import CommitMessageParser

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'proman-source'
__description__ = 'Convenience tools to manage SCM systems with Python.'
__version__ = '0.1.0'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2020 Jesse Johnson.'

repo = Repo('.')
source_config = Config(filepath=os.path.join(os.getcwd(), 'pyproject.toml'))
parser = CommitMessageParser()

__all__ = ['repo', 'source_config', 'parser']
