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
    result = runner.invoke(main, ['text', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main text [OPTIONS] TEXT')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['txt', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main txt [OPTIONS] TEXT')


def test_debug_option_prints_kwargs(runner):
    params = '--debug text sometext'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.TeXT {")


def test_one_text_record_created(runner):
    params = 'text one'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd1\x01\x06T\x02enone'


def test_two_text_records_created(runner):
    params = 'text one text two'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\x91\x01\x06T\x02enoneQ\x01\x06T\x02entwo'


def test_default_text_language(runner):
    params = 'text English'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd1\x01\nT\x02enEnglish'


def test_specific_text_language(runner):
    params = 'text --language de German'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd1\x01\tT\x02deGerman'
