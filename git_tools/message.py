# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

import logging
import os

from lark import Lark, logger

grammar_path = os.path.join('git_tools', 'grammars', 'conventional_commits.lark')

message = '''fix(example): test a message

test body of comment 1 test
test body of comment 2 test
'''

parser = Lark.open(grammar_path, start='message', debug=True)
print(parser.parse(message).pretty())
