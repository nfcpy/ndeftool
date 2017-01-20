# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import pytest
from ndeftool.cli import main


@pytest.fixture
def runner():
    import click.testing
    return click.testing.CliRunner()


@pytest.yield_fixture
def isolated_runner(runner):
    with runner.isolated_filesystem():
        yield runner


def test_help_option_prints_usage(runner):
    result = runner.invoke(main, ['identifier', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main identifier [OPTIONS] NAME')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['id', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main id [OPTIONS] NAME')


def test_debug_option_prints_kwargs(runner):
    params = '--debug identifier name'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.IDentifier {")


def test_identifier_as_first_command(runner):
    params = 'identifier name'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xdd\x00\x00\x04name'


def test_identifier_as_second_command(runner):
    params = 'typename text/plain identifier name'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xda\n\x00\x04text/plainname'


def test_very_long_name_raises_error(runner):
    result = runner.invoke(main, ['id', 256*'0'])
    assert result.exit_code == 1
    assert 'Error:' in result.output
