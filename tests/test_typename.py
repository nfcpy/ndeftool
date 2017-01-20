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
    result = runner.invoke(main, ['typename', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main typename [OPTIONS] TYPE')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['tn', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main tn [OPTIONS] TYPE')


def test_debug_option_prints_kwargs(isolated_runner):
    params = '--debug typename text/plain'.split()
    result = isolated_runner.invoke(main, params, input='')
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.TypeName {")


def test_typename_as_first_command(runner):
    params = 'typename text/plain'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd2\n\x00text/plain'


def test_typename_as_second_command(runner):
    params = 'identifier name typename text/plain'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xda\n\x00\x04text/plainname'


def test_invalid_type_raises_error(runner):
    params = '--silent typename invalid-type'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 1
    assert 'Error:' in result.output


def test_payload_type_error_raises_error(runner):
    params = '--silent payload helloworld typename urn:nfc:wkt:T'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 1
    assert 'Error:' in result.output


def test_payload_type_error_not_checked(runner):
    params = 'payload helloworld typename --no-check urn:nfc:wkt:T'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd1\x01\nThelloworld'
