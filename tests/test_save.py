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


plain_text_records = [
    b'\x9a\n\x0b\x02text/plainR1Hello World',
    b'\x1a\n\x0b\x02text/plainR2Hello World',
    b'\x1a\n\x0b\x02text/plainR3Hello World',
    b'\x1a\n\x0b\x02text/plainR4Hello World',
    b'Z\n\x0b\x02text/plainR5Hello World']


def test_help_option_prints_usage(runner):
    result = runner.invoke(main, ['save', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main save [OPTIONS] PATH')


def test_abbreviated_command_name(runner):
    result = runner.invoke(main, ['s', '--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: main s [OPTIONS] PATH')


def test_debug_option_prints_kwargs(isolated_runner):
    params = '--debug save text.ndef'.split()
    result = isolated_runner.invoke(main, params, input='')
    assert result.exit_code == 0
    assert result.output.startswith("ndeftool.commands.Save {")


def test_read_from_standard_input(isolated_runner):
    octets = b'\xda\n\x0b\x02text/plainR1Hello World'
    params = 'save hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == octets


def test_read_from_stdin_with_errors(isolated_runner):
    octets = b'\x9a\n\x0b\x02text/plainR1Hello World'
    params = 'save hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 1
    assert "Error:" in result.output
    params = '--relax save hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == b'\xda' + octets[1:]


def test_read_from_message_pipe(isolated_runner):
    octets = b'\xda\n\x0b\x02text/plainR1Hello World'
    params = 'save --keep hello1.ndef save hello2.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello1.ndef', 'rb').read() == octets
    assert open('hello2.ndef', 'rb').read() == octets


def test_save_all_records_to_one_file(isolated_runner):
    octets = b''.join(plain_text_records)
    params = 'save hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == octets


def test_save_first_record_with_head(isolated_runner):
    octets = b''.join(plain_text_records)
    params = 'save --head 1 hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == \
        b'\xda' + plain_text_records[0][1:]


def test_save_first_record_with_count(isolated_runner):
    octets = b''.join(plain_text_records)
    params = 'save --count 1 hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == \
        b'\xda' + plain_text_records[0][1:]


def test_save_last_record_with_tail(isolated_runner):
    octets = b''.join(plain_text_records)
    params = 'save --tail 1 hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == \
        b'\xda' + plain_text_records[-1][1:]


def test_save_last_record_with_skip(isolated_runner):
    toskip = len(plain_text_records) - 1
    octets = b''.join(plain_text_records)
    params = 'save --skip {} hello.txt.ndef'.format(toskip).split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == \
        b'\xda' + plain_text_records[-1][1:]


def test_save_skip_count_head_tail(isolated_runner):
    assert len(plain_text_records) == 5
    octets = b''.join(plain_text_records)
    params = 'save --skip 1 --count 3 --head 2 --tail 1 hello.txt.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.txt.ndef', 'rb').read() == \
        b'\xda' + plain_text_records[2][1:]


def test_save_do_not_overwrite_file(isolated_runner):
    open('hello.ndef', 'wb')
    octets = b''.join(plain_text_records)
    params = 'save hello.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 1
    assert "Error: path 'hello.ndef' exists." in result.output


def test_save_force_overwrite_file(isolated_runner):
    open('hello.ndef', 'wb')
    octets = b''.join(plain_text_records)
    params = 'save --force hello.ndef'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert open('hello.ndef', 'rb').read() == octets


def test_burst_records_to_files(isolated_runner):
    octets = b''.join(plain_text_records)
    params = 'save --burst hello'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    for index in range(len(plain_text_records)):
        assert open('hello/%03d.ndef' % index, 'rb').read() == \
            b'\xda' + plain_text_records[index][1:]


def test_unpack_records_to_files(isolated_runner):
    octets = b''.join(plain_text_records)
    params = 'save --unpack hello'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    for index in range(len(plain_text_records)):
        assert open('hello/R%d' % (index+1)).read() == "Hello World"


def test_unpack_force_remove_dir(isolated_runner):
    os.mkdir('hello')
    for index in range(len(plain_text_records)):
        open('hello/R%d' % (index+1), 'w')
    octets = b''.join(plain_text_records)
    params = 'save --force --unpack hello'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    for index in range(len(plain_text_records)):
        assert open('hello/R%d' % (index+1)).read() == "Hello World"


def test_unpack_record_without_name(isolated_runner):
    octets = b'\xda\n\x0b\x00text/plainHello World'
    params = 'save --unpack hello'.split()
    result = isolated_runner.invoke(main, params, input=octets)
    assert result.exit_code == 0
    assert "Skipping 1 record without name" in result.output
