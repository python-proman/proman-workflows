from packaging.version import _parse_letter_version, _parse_local_version

v1 = _parse_letter_version('alpha', 2)
print(type(v1), v1)

v2 = _parse_local_version('build.4')
print(type(v2), v2)
