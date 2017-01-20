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
    result = runner.invoke(main, ['uri', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main uri [OPTIONS] RESOURCE')


def test_debug_option_prints_kwargs(runner):
    params = '--debug uri http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.URI {")


def test_one_uri_record_created(runner):
    params = 'uri http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd1\x01\nU\x03nfcpy.org'


def test_two_uri_records_created(runner):
    params = 'uri http://nfcpy.org uri tel:123'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\x91\x01\nU\x03nfcpy.orgQ\x01\x04U\x05123'
