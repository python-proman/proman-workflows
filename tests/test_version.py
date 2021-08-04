# type: ignore
'''Add version tests.'''
from proman_workflows import __version__


def test_version():
    '''Test version.'''
    assert __version__ == "0.1.0"
