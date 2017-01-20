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
    result = runner.invoke(main, ['payload', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main payload [OPTIONS] DATA')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['pl', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main pl [OPTIONS] DATA')


def test_debug_option_prints_kwargs(isolated_runner):
    params = '--debug payload DATA'.split()
    result = isolated_runner.invoke(main, params, input='')
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.PayLoad {")


def test_payload_as_first_command(runner):
    params = 'payload helloworld'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd5\x00\nhelloworld'


def test_payload_as_second_command(runner):
    params = 'typename text/plain payload helloworld'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd2\n\ntext/plainhelloworld'


def test_payload_makes_decode_error(runner):
    params = '--silent load - payload helloworld'.split()
    result = runner.invoke(main, params, input=b'\xd1\x01\x03T\x02en')
    assert result.exit_code == 1
    assert 'Error:' in result.output


def test_payload_error_not_checked(runner):
    params = '--silent load - payload --no-check helloworld'.split()
    result = runner.invoke(main, params, input=b'\xd1\x01\x03T\x02en')
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd1\x01\nThelloworld'
