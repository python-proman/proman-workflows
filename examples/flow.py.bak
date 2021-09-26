import pytest
from transitions.core import MachineError

from proman_workflows import repo
from proman_workflows.vcs import GitFlow

workflow = GitFlow(repo, branch='feat-test-123')
assert workflow.get_initial_state() == 'feature'
workflow.state == 'feature'

workflow.feature_finish()
workflow.state == 'develop'

workflow.release_start()
workflow.state == 'release'

workflow.release_finish()
workflow.state == 'master'

workflow.hotfix_start()
workflow.state == 'hotfix'

workflow.hotfix_finish()
workflow.state == 'master'

with pytest.raises(MachineError):
    workflow.release_finish()
