"""Test GPG capability."""

from typing import TYPE_CHECKING, Any, Dict, List

import pytest

from workflows.pki import gpg

if TYPE_CHECKING:
    from invoke import Context


@pytest.mark.parametrize(
    'settings',
    [
        {
            'key_type': 'RSA',
            'key_length': 4096,
            'subkey_type': 'RSA',
            'subkey_length': 2048,
        },
        {
            'key_type': 'ECDSA',
            'key_curve': 'nistp256',
            'subkey_type': 'ECDSA',
            'subkey_curve': 'nistp256',
            'subkey_usage': ['sign'],
        },
        {
            'key_type': 'EDDSA',
            'key_curve': 'ed25519',
            'subkey_type': 'EDDSA',
            'subkey_curve': 'ed25519',
            'subkey_usage': ['sign'],
        }
    ]
)
def test_key_generation(
    gpgctx: 'Context', settings: List[Dict[str, Any]]
) -> None:
    """Test that key generation handles invalid key type."""
    result = gpg.gen_key(
        gpgctx,
        name='Test Name',
        email='test.name@example.com',
        comment='A test user',
        password='password',
        expire_date='1d',
        **settings
    )
    assert result is not None
    # assert result.fingerprint is not None
