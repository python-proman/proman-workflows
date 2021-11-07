"""Add version tests."""
from protools import __version__


def test_version() -> None:
    """Test version."""
    assert __version__ == '0.1.0'
