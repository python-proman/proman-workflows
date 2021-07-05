# type: ignore
from proman_workflows.version import PythonVersion

vx = PythonVersion('1.0.0')

vx.start_local()
print(vx, vx.local)

vx.bump_local()
print(vx)
