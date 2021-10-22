"""Configure integration tests."""

import os
import shutil
from typing import TYPE_CHECKING

import pytest
from invoke import MockContext
from gnupg import GPG

if TYPE_CHECKING:
    from invoke import Context


@pytest.fixture
def gpgctx() -> 'Context':
    """Manage GPG context."""
    ctx = MockContext()
    gnupghome = os.path.join(os.path.dirname(__file__), '.gnupg')
    if not os.path.exists(gnupghome):
        os.mkdir(gnupghome, 0o700)
    ctx.__gpg = GPG(gnupghome=gnupghome)
    yield ctx
    shutil.rmtree(gnupghome)
