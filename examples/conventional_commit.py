# from proman_workflows.release import ReleaseController
from proman_workflows import get_release_controller

controller = get_release_controller()
print(controller.config.retrieve('/tool/proman/release/files'))
print('old', controller.version)
controller.bump_version()
print('new', controller.version)
