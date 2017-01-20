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
    result = runner.invoke(main, ['smartposter', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith(
        'Usage: main smartposter [OPTIONS] RESOURCE')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['smp', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main smp [OPTIONS] RESOURCE')


def test_debug_option_prints_kwargs(runner):
    params = '--debug smartposter http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.SMartPoster {")


def test_smartposter_with_no_options(runner):
    params = 'smartposter http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == b'\xd1\x02\x0eSp\xd1\x01\nU\x03nfcpy.org'


def test_two_smartposter_commands(runner):
    params = 'smartposter http://nfcpy.org smartposter tel:12'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == \
        b'\x91\x02\x0eSp\xd1\x01\nU\x03nfcpy.orgQ\x02\x07Sp\xd1\x01\x03U\x0512'


def test_smartposter_with_english_title(runner):
    params = 'smartposter -T Title http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == \
        b'\xd1\x02\x1aSp\x91\x01\nU\x03nfcpy.orgQ\x01\x08T\x02enTitle'


def test_smartposter_with_german_title(runner):
    params = 'smartposter -t de Titel http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == \
        b'\xd1\x02\x1aSp\x91\x01\nU\x03nfcpy.orgQ\x01\x08T\x02deTitel'


def test_smartposter_with_two_titles(runner):
    params = 'smartposter -T Title -t de Titel http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == \
        b'\xd1\x02&Sp\x91\x01\nU\x03nfcpy.org' \
        b'\x11\x01\x08T\x02deTitelQ\x01\x08T\x02enTitle'


def test_smartposter_with_action_exec(runner):
    params = 'smartposter -a exec http://nfcpy.org'.split()
    result = runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == \
        b'\xd1\x02\x15Sp\x91\x01\nU\x03nfcpy.orgQ\x03\x01act\x00'


def test_smartposter_with_png_icon(isolated_runner):
    icon_1x1_png_data = bytearray.fromhex(
        '89504e470d0a1a0a0000000d494844520000000100000001080200000090'
        '7753de0000000c4944415408d763f8ffff3f0005fe02fedccc59e7000000'
        '0049454e44ae426082')
    open('1x1.png', 'wb').write(icon_1x1_png_data)
    params = 'smartposter -i 1x1.png http://nfcpy.org'.split()
    result = isolated_runner.invoke(main, params)
    assert result.exit_code == 0
    assert result.output_bytes == (
        b'\xd1\x02_Sp\x91\x01\nU\x03nfcpy.orgR\tEimage/png\x89PNG\r\n\x1a\n'
        b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00'
        b'\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05'
        b'\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82')


def test_smartposter_with_invalid_icon(isolated_runner):
    open('1x1.png', 'w').write('this is not a png file')
    params = 'smartposter -i 1x1.png http://nfcpy.org'.split()
    result = isolated_runner.invoke(main, params)
    assert result.exit_code == 1
    assert "Error:" in result.output
