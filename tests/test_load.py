# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import os
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
    result = runner.invoke(main, ['load', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main load [OPTIONS] PATH')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['l', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main l [OPTIONS] PATH')


def test_debug_option_prints_kwargs(runner):
    params = '--debug load -'.split()
    result = runner.invoke(main, params, input='')
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.Load {")


def test_pack_from_standard_input(runner):
    result = runner.invoke(main, ['load', '--pack', '-'], input=b"Hello World")
    assert result.exit_code == 0
    assert result.output_bytes == b'\xda\n\x0b\x07text/plain<stdin>Hello World'


def test_pack_from_full_file_path(isolated_runner):
    open('hello.txt', 'w').write('Hello World')
    result = isolated_runner.invoke(main, ['load', '--pack', 'hello.txt'])
    assert result.exit_code == 0
    assert result.output_bytes == b'\xda\n\x0b\ttext/plainhello.txtHello World'


def test_pack_from_glob_file_path(isolated_runner):
    open('hello.txt', 'w').write('Hello World')
    result = isolated_runner.invoke(main, ['load', '--pack', '*.txt'])
    assert result.exit_code == 0
    assert result.output_bytes == b'\xda\n\x0b\ttext/plainhello.txtHello World'


def test_pack_glob_multiple_files(isolated_runner):
    open('hello1.txt', 'w').write('Hello World')
    open('hello2.txt', 'w').write('World Hello')
    result = isolated_runner.invoke(main, ['load', '--pack', 'hello?.txt'])
    assert result.exit_code == 0
    assert result.output_bytes == \
        b'\x9a\n\x0b\ntext/plainhello1.txtHello World' \
        b'Z\n\x0b\ntext/plainhello2.txtWorld Hello'


def test_pack_pipe_multiple_files(isolated_runner):
    open('hello1.txt', 'w').write('Hello World')
    open('hello2.txt', 'w').write('World Hello')
    command = 'load --pack hello1.txt load --pack hello2.txt'
    result = isolated_runner.invoke(main, command.split())
    assert result.exit_code == 0
    assert result.output_bytes == \
        b'\x9a\n\x0b\ntext/plainhello1.txtHello World' \
        b'Z\n\x0b\ntext/plainhello2.txtWorld Hello'


def test_load_from_standard_input(runner):
    octets = b'\xda\n\x0b\x07text/plain<stdin>Hello World'
    params = '--silent load -'
    result = runner.invoke(main, params.split(), input=octets)
    assert result.exit_code == 0
    assert result.output_bytes == octets


def test_load_from_full_file_path(isolated_runner):
    octets = b'\xda\n\x0b\x09text/plainhello.txtHello World'
    open('hello.txt.ndef', 'wb').write(octets)
    params = '--silent load hello.txt.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output_bytes == octets


def test_load_from_glob_file_path(isolated_runner):
    octets = b'\xda\n\x0b\ttext/plainhello.txtHello World'
    open('hello.txt.ndef', 'wb').write(octets)
    params = '--silent load *.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output_bytes == octets


def test_pack_load_multiple_files(isolated_runner):
    octets1 = b'\xda\n\x0b\ntext/plainhello1.txtHello World'
    octets2 = b'\xda\n\x0b\ntext/plainhello2.txtWorld Hello'
    open('hello1.txt.ndef', 'wb').write(octets1)
    open('hello2.txt.ndef', 'wb').write(octets2)
    params = '--silent load hello?.txt.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output_bytes == b'\x9a' + octets1[1:] + b'\x5a' + octets2[1:]


def test_load_pipe_multiple_files(isolated_runner):
    octets1 = b'\xda\n\x0b\ntext/plainhello1.txtHello World'
    octets2 = b'\xda\n\x0b\ntext/plainhello2.txtWorld Hello'
    open('hello1.txt.ndef', 'wb').write(octets1)
    open('hello2.txt.ndef', 'wb').write(octets2)
    params = '--silent load hello1.txt.ndef load hello2.txt.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output_bytes == b'\x9a' + octets1[1:] + b'\x5a' + octets2[1:]


def test_load_strict_then_relax(isolated_runner):
    octets = b'\x1a\n\x0b\ttext/plainhello.txtHello World'
    open('hello.txt.ndef', 'wb').write(octets)
    params = '--silent load hello.txt.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 1
    assert result.output.startswith(
        'Error: hello.txt.ndef does not contain a valid NDEF message.')
    params = '--relax ' + params
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output_bytes == b'\xda' + octets[1:]


def test_load_relax_then_ignore(isolated_runner):
    octets1 = b'\xda\n\xff\ntext/plainhello1.txtHello World'
    octets2 = b'\x1a\n\x0b\ntext/plainhello2.txtWorld Hello'
    open('hello1.txt.ndef', 'wb').write(octets1)
    open('hello2.txt.ndef', 'wb').write(octets2)
    params = '--relax --silent load hello1.txt.ndef load hello2.txt.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 1
    assert result.output.startswith(
        'Error: hello1.txt.ndef does not contain a valid NDEF message.')
    params = '--ignore --silent load hello1.txt.ndef load hello2.txt.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output_bytes == b'\xda' + octets2[1:]


def test_no_files_selected_by_path(isolated_runner):
    params = 'load hello.txt.ndef load *.txt.ndef'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output.splitlines() == [
        "No files selected by path 'hello.txt.ndef'.",
        "No files selected by path '*.txt.ndef'.",
    ]


def test_permission_denied_error(isolated_runner):
    open('hello.txt', 'w').write("Hello World")
    os.chmod('hello.txt', 0)
    params = 'load --pack *.txt'
    result = isolated_runner.invoke(main, params.split())
    assert result.exit_code == 0
    assert result.output == "[Errno 13] Permission denied: 'hello.txt'\n"
