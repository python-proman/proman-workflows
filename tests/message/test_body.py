'''Test git hooks pipeline.'''

from git_tools.message import MessageParser
from textwrap import dedent

message = '''fix: test a message

test body of comment test
test body of comment 2 test
'''


def test_body_message():
    '''test body breaking change.'''
    parser = MessageParser()
    parser.parse(message)
    assert parser.body[0] == 'test body of comment test'
    assert parser.body[1] == 'test body of comment 2 test'
