# from proman_workflows.controller import IntegrationController
from proman_workflows import get_release_controller

# controller = get_release_controller()
# print(controller.config.retrieve('/tool/proman/release/files'))
# print('old', controller.version)
#
# controller.bump_version()
# print('new', controller.version)


kind = get_release_controller(version='1.0.0')
kind.parse('fix: test')
print(kind.bump_version())

scope = get_release_controller(version='1.0.0')
scope.parse('feat(ui): test')
print(scope.bump_version())

refactor = get_release_controller(version='1.0.0')
refactor.parse('refactor!: test')
print(refactor.bump_version())

controller = get_release_controller(version='1.2.0')
assert str(controller.version) == '1.2.0'
print(controller.bump_version())
