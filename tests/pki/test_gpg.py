"""Test GPG capability."""

from invoke import MockContext, Result

from proman_workflows.pki import gpg


def test_key_generation() -> None:
    """Test that key generation handles invalid key type."""
    ctx = MockContext(run=Result('B71406AE172A63177432B25BA8B276998469F5A1'))
    result = gpg.gen_key(
        ctx,
        name='Test Name',
        email='test.name@example.com',
        comment='A test user',
        password='',
        key_type='RSA',
        key_length=4096,
        # 'subkey_type='ELG-E',
        # 'subkey_length=2048,
        expire_date=0,
    )
    print(result.__dict__)
    assert result.fingerprint == 'B71406AE172A63177432B25BA8B276998469F5A1'
