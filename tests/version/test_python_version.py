# type: ignore
from proman_workflows.version import PythonVersion


def test_releaese():
    v1 = PythonVersion('1.0.0')
    assert v1.get_state() == 'final'
    assert v1.major == 1
    assert v1.minor == 0
    assert v1.micro == 0
    v1.bump_major()
    assert str(v1) == '2.0.0'
    v1.bump_minor()
    assert str(v1) == '2.1.0'
    v1.bump_micro()
    assert str(v1) == '2.1.1'


def test_prerelease():
    v2 = PythonVersion('2.0.0', enable_prereleases=True)
    assert v2.get_state() == 'final'
    v2.start_prerelease()
    assert str(v2) == '3.0.0a0'
    assert v2.pre == ('a', 0)
    v2.bump_prerelease()
    assert str(v2) == '3.0.0a1'
    v2.new_prerelease()
    assert str(v2) == '3.0.0b0'
    v2.bump_prerelease()
    assert str(v2) == '3.0.0b1'
    v2.new_prerelease()
    assert str(v2) == '3.0.0rc0'
    v2.bump_prerelease()
    assert str(v2) == '3.0.0rc1'


def test_post():
    v3 = PythonVersion('2.0.0-post1', enable_postreleases=True)
    assert v3.get_state() == 'post'
    assert v3.release == (2, 0, 0)
    assert v3.base_version == '2.0.0'
    assert v3.major == 2
    assert v3.minor == 0
    assert v3.micro == 0
    v3.bump_major()
    assert str(v3) == '3.0.0'
    assert v3.major == 3
    v3.bump_minor()
    assert str(v3) == '3.1.0'
    assert v3.minor == 1
    v3.bump_micro()
    assert str(v3) == '3.1.1'
    assert v3.micro == 1


def test_local():
    v4 = PythonVersion('3.0.0+dev4.post3')
    v4.get_state() == 'final'
    assert v4.release == (3, 0, 0)
    assert v4.pre is None
    assert v4.post is None
    assert v4.local == 'dev4.post3'
    v4.bump_major()
    assert str(v4) == '4.0.0'


def test_mixed():
    v5 = PythonVersion('5.0.0-rc5+build254')
    print('v5', v5.get_state())
    print('v5', v5.local)


def test_epoch():
    v6 = PythonVersion('1!6.0.0')
    assert v6.get_state() == 'final'
    assert v6.epoch == 1
    v6.bump_epoch()
    assert str(v6) == '2!6.0.0'
