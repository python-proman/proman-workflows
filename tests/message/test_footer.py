'''Test git hooks pipeline.'''

from git_tools.message import MessageParser

message = '''fix(example): test a message

Reviewed-by: Jim H. Henson Jr. <jim.henson1@email.com>
Refs #123
Fix #124
BREAKING CHANGE: This could change things
'''


def test_footer_trailer():
    '''Test footer trailer.'''
    parser = MessageParser()
    parser.parse(message)
    assert parser.footer['trailer']['token'] == 'Reviewed-by'
    assert parser.footer['trailer']['name'] == 'Jim H. Henson Jr.'
    assert parser.footer['trailer']['email'] == 'jim.henson1@email.com'


def test_footer_issues():
    '''Test footer issues.'''
    parser = MessageParser()
    parser.parse(message)
    assert parser.footer['issues'][0]['Refs'] == '123'
    assert parser.footer['issues'][1]['Fix'] == '124'


def test_footer_breaking_change():
    '''test footer breaking change.'''
    parser = MessageParser()
    parser.parse(message)
    assert parser.footer['breaking_change'] == 'This could change things'
