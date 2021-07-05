# type: ignore
from proman_workflows.version import PythonVersion

vx = PythonVersion(
    '1.0.0',
    enable_devreleases=True,
    enable_prereleases=True,
    enable_postreleases=True,
)
vx.start_local()
print(vx)
vx.finalize_release()
print(vx)
vx.start_devrelease()
print(vx)
vx.finalize_release()
print(vx)
print('preleases only happen on major releases')
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.finalize_release()
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
vx.finalize_release()
print(vx)
vx.start_devrelease()
print(vx)
vx.finalize_release()
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
vx.finalize_release()
print(vx)
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.start_prerelease()
print(vx, vx.get_state())
vx.finalize_release()
print(vx, vx.get_state())
vx.start_postrelease()
print(vx, vx.get_state())
vx.bump_micro()
print(vx)
