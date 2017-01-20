# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import sys
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
    result = runner.invoke(main, ['print', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main print [OPTIONS]')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['p', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main p [OPTIONS]')


def test_debug_option_prints_kwargs(isolated_runner):
    params = '--debug print'.split()
    result = isolated_runner.invoke(main, params, input='')
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.Print {")


def test_read_from_standard_input(runner):
    octets = b'\xda\n\x0b\x02text/plainR1Hello World'
    params = 'print'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert "NDEF Record TYPE 'text/plain' ID 'R1' PAYLOAD 11" in result.output


def test_read_from_stdin_with_errors(runner):
    octets = b'\x1a\n\x0b\x02text/plainR1Hello World'
    params = 'print'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 1
    assert "Error:" in result.output
    params = '--relax print'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert "NDEF Record TYPE 'text/plain' ID 'R1' PAYLOAD 11" in result.output


def test_read_from_message_pipe(runner):
    octets = b'\xda\n\x0b\x02text/plainR1Hello World'
    params = '--silent print --keep print'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 2
    assert result.output.splitlines()[0].startswith("NDEF Record")
    assert result.output.splitlines()[1].startswith("NDEF Record")


def test_long_print_generic_record(runner):
    octets = b'\xda\x09\x0a\x02some/mimeR1HelloWorld'
    params = '--silent print --long'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    output = result.output.splitlines()
    assert len(output) == 4
    assert output[0] == "Record [record #1]"
    assert output[1].split() == ["type", "some/mime"]
    assert output[2].split() == ["name", "R1"]
    if sys.version_info.major > 2:
        assert output[3].split() == ["data", "b'HelloWorld'"]
    else:
        assert output[3].split() == ["data", "HelloWorld"]


def test_long_print_text_record(runner):
    octets = b'\xd1\x01\x06T\x02enone'
    params = '--silent print --long'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    output = result.output.splitlines()
    assert len(output) == 4
    assert output[0] == "NFC Forum Text Record [record #1]"
    assert output[1].split() == ["content", "one"]
    assert output[2].split() == ["language", "en"]
    assert output[3].split() == ["encoding", "UTF-8"]


def test_long_print_uri_record(runner):
    octets = b'\xd1\x01\nU\x03nfcpy.org'
    params = '--silent print --long'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    output = result.output.splitlines()
    assert len(output) == 2
    assert output[0] == "NFC Forum URI Record [record #1]"
    assert output[1].split() == ["resource", "http://nfcpy.org"]


def test_long_print_smartposter_1(runner):
    octets = b'\xd1\x02\x0eSp\xd1\x01\nU\x03nfcpy.org'
    params = '--silent print --long'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    output = result.output.splitlines()
    assert len(output) == 2
    assert output[0] == "NFC Forum Smart Poster Record [record #1]"
    assert output[1].split() == ["resource", "http://nfcpy.org"]


def test_long_print_smartposter_2(runner):
    octets = b'\xd1\x02\x1aSp\x91\x01\nU\x03nfcpy.orgQ\x01\x08T\x02enTitle'
    params = '--silent print --long'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    output = result.output.splitlines()
    assert len(output) == 3
    assert output[0] == "NFC Forum Smart Poster Record [record #1]"
    assert output[1].split() == ["resource", "http://nfcpy.org"]
    assert output[2].split() == ["title_en", "Title"]


def test_long_print_smartposter_3(runner):
    octets = b'\xd1\x02\x15Sp\x91\x01\nU\x03nfcpy.orgQ\x03\x01act\x00'
    params = '--silent print --long'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    output = result.output.splitlines()
    print(result.output)
    assert len(output) == 3
    assert output[0] == "NFC Forum Smart Poster Record [record #1]"
    assert output[1].split() == ["resource", "http://nfcpy.org"]
    assert output[2].split() == ["action", "exec"]


def test_long_print_smartposter_4(runner):
    octets = (
        b'\xd1\x02_Sp\x91\x01\nU\x03nfcpy.orgR\tEimage/png\x89PNG\r\n\x1a\n'
        b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00'
        b'\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05'
        b'\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    params = '--silent print --long'.split()
    result = runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    output = result.output.splitlines()
    print(result.output)
    assert len(output) == 3
    assert output[0] == "NFC Forum Smart Poster Record [record #1]"
    assert output[1].split() == ["resource", "http://nfcpy.org"]
    assert output[2].split() == ["image/png", "69", "byte"]
