"""Test git hooks pipeline."""

import sys

import pytest

try:
    from pypyr import log, pipelinerunner
except ImportError:
    pass


@pytest.mark.skipif(
    'pipelinerunner' not in sys.modules, reason='requires the PyPyr library'
)
def test_hooks_pre_commit() -> None:
    """Test pre-commit hooks using PyPyr."""
    log.logger.set_root_logger(log_level=25, log_path=None)

    pipelinerunner.main(
        pipeline_name='.workflows',
        pipeline_context_input='arb context input',
        working_dir='tests/hooks',
        groups=['pre-commit'],
        success_group='pre-commit-success',
        failure_group='pre-commit-failure',
    )
