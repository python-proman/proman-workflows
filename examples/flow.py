from proman_workflows import repo
from proman_workflows.release import GitFlow

workflow = GitFlow(repo, branch='feat-test-123')
# print('state', workflow.working_branch())
print('state', workflow.state)

workflow.feature_finish()
print('state', workflow.state)

workflow.release_start()
print('state', workflow.state)

workflow.release_finish()
print('state', workflow.state)

workflow.hotfix_start()
print('state', workflow.state)

workflow.hotfix_finish()
print('state', workflow.state)
