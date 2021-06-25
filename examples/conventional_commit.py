from proman_workflows.release import CommitMessageAction


commit = CommitMessageAction()
print(commit.config.retrieve('/tool/proman/release/files'))
print(commit.version)
print(commit.bump_version())
