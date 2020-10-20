'''Test git hooks pipeline.'''
from pypyr import log, pipelinerunner


def test_hooks_pre_commit():
    '''Test pre-commit hooks.'''
    log.logger.set_root_logger(
        log_level=25,
        log_path=None
    )
    
    pipelinerunner.main(
        pipeline_name='.git-hooks',
        pipeline_context_input='arb context input',
        working_dir='tests/hooks',
        groups=['pre-commit'],
        success_group='pre-commit-success',
        failure_group='pre-commit-failure'
    )
