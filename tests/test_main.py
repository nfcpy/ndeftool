# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import pytest
from ndeftool.cli import main


@pytest.fixture
def runner():
    import click.testing
    return click.testing.CliRunner()


def test_no_command_prints_usage(runner):
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert result.output.startswith(
        'Usage: main [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...')


def test_help_option_prints_usage(runner):
    result = runner.invoke(main, ['--help', 'unknown-command'])
    assert result.exit_code == 0
    assert result.output.startswith(
        'Usage: main [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...')


def test_unknown_command_prints_error(runner):
    result = runner.invoke(main, ['unknown-command'])
    assert result.exit_code == 2
    assert result.output.startswith(
        'Usage: main [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...')
    assert "Error:" in result.output
