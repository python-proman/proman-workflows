'''Test git hooks pipeline.'''

from git_tools.message import MessageParser


def test_title():
    parser = MessageParser()
    parser.parse('fix: test')
    assert parser.title['type'] == 'fix'
    assert parser.title['description'] == 'test'


def test_title_scope():
    parser = MessageParser()
    parser.parse('feat(ui): test')
    assert parser.title['type'] == 'feat'
    assert parser.title['scope'] == 'ui'
    assert parser.title['description'] == 'test'


def test_title_breaking_change():
    parser = MessageParser()
    parser.parse('refactor!: test')
    assert parser.title['type'] == 'refactor'
    assert parser.title['break'] is True
    assert parser.title['description'] == 'test'
