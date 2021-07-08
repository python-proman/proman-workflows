# type: ignore
from proman_workflows.version import PythonVersion

lcl = PythonVersion('1.0.0')

lcl.start_local()
assert lcl.local == 'build.0'

lcl.bump_local()
assert lcl.local == 'build.1'

vx = PythonVersion(
    '1.0.0',
    enable_devreleases=True,
    enable_prereleases=True,
    enable_postreleases=True,
)
vx.start_local()
print(vx)
vx.finish_release()
print(vx)
vx.start_devrelease()
print(vx)
vx.finish_release()
print(vx)
print('preleases only happen on major releases')
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.finish_release()
print(vx, vx.get_state())
vx.start_postrelease()
print(vx, vx.get_state())
vx.bump_micro()
print(vx)

vx = PythonVersion(
    '1.0.0',
    enable_devreleases=True,
    enable_postreleases=True,
)
vx.start_local()
print(vx)
vx.finish_release()
print(vx)
vx.start_devrelease()
print(vx)
vx.finish_release()
print(vx, vx.get_state())
vx.start_postrelease()
print(vx, vx.get_state())
vx.bump_micro()
print(vx)

vx = PythonVersion(
    '1.0.0',
    enable_prereleases=True,
    enable_postreleases=True,
)
vx.start_local()
print(vx)
vx.finish_release()
print(vx)
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.finish_release()
print(vx, vx.get_state())
vx.start_postrelease()
print(vx, vx.get_state())
vx.bump_micro()
print(vx)
