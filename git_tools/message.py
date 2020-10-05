# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

import logging
import os

from lark import Lark, logger, Transformer

grammar_path = os.path.join('git_tools', 'grammars', 'conventional_commits.lark')

message = '''fix(example)!: test a message

test body of comment test
test body of comment 2 test

Reviewed-by: Jesse <jpj6652@gmail.com>
Refs #123
Refs #124
BREAKING CHANGE: This could change things
'''

class MessageTransformer(Transformer):
    def title(self, args):
        title = {}
        for arg in args:
            title[arg.data] = next((x for x in arg.children), True)
        return title

    def body(self, args=None):
        return [arg.value for arg in args]

    def footer(self, args=None):
        footer = {}
        for arg in args:
            if arg.data == 'trailer':
                footer['trailer'] = {}
                for x in arg.children:
                    print(x.data, [arg for arg in args][0])
                    # footer['trailer'][x.data] = [arg for arg in args][0]
        print('footer:', footer)
        return args

parser = Lark.open(grammar_path, start='message', debug=True)
print(parser.parse(message).pretty())
tree = parser.parse(message)
MessageTransformer().transform(tree=tree)
