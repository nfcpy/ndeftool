# -*- coding: utf-8 -*-

from functools import wraps
import os.path
import click
import ndef

version_message = '%%(prog)s %%(version)s (ndeflib %s)' % ndef.__version__
command_plugins = os.path.join(os.path.dirname(__file__), 'commands')


def echo(*args, **kwargs):
    click.echo(*args, **kwargs)


def info(*args):
    if click.get_current_context().meta['output-logmsg'] != 'silent':
        click.secho(*args, err=True, fg='green')


def dmsg(*args):
    if click.get_current_context().meta['output-logmsg'] == 'debug':
        click.secho(*args, err=True, fg='yellow')


def warn(*args):
    click.secho(*args, err=True, fg='red')


class CommandGroup(click.Group):
    def list_commands(self, ctx):
        command_list = []

        # All commands are separate Python files within the
        # command_plugins folder.
        for filename in sorted(os.listdir(command_plugins)):
            basename, extension = os.path.splitext(filename)
            if extension == '.py' and basename != '__init__':
                command_list.append(basename)

        return command_list

    def get_command(self, ctx, name):
        name = name.lower()  # all commands treated case insensitive

        # From list_commands() we get the command file names without
        # extension. We use the upper case letters to construct the
        # abbreviated name and import the module if the requested
        # command name matches either the lower case full or short
        # name.
        for cmd_name in self.list_commands(ctx):
            cmd_abbr = ''.join(x for x in cmd_name if 'A' <= x <= 'Z')
            if name in (cmd_name.lower(), cmd_abbr.lower()):
                module = 'ndeftool.commands.' + cmd_name
                return __import__(module, None, None, ['cmd']).cmd

    def format_commands(self, ctx, formatter):
        rows = []

        # From list_commands() we get the command file names without
        # extension. We use the upper case letters to construct the
        # abbreviated name and store lower case versions of short and
        # long command name.
        for cmd_name in self.list_commands(ctx):
            cmd_abbr = ''.join(x for x in cmd_name if 'A' <= x <= 'Z')
            cmd_help = self.get_command(ctx, cmd_name).short_help or ''
            rows.append((cmd_abbr.lower(), cmd_name.lower(), cmd_help))

        # We want the command list to be sorted by abbreviated command
        # name with the shortest names first.
        rows = sorted(rows, key=lambda x: '%02d %s' % (len(x[0]), x[0]))
        rows = [('%s, %s' % (a, n) if a != n else a, h) for a, n, h in rows]

        with formatter.section('Commands'):
            formatter.write_dl(rows)


@click.command(cls=CommandGroup, chain=True)
@click.version_option(message=version_message)
@click.option('--relax', 'errors', flag_value='relax',
              help='Ignore some errors when decoding.')
@click.option('--ignore', 'errors', flag_value='ignore',
              help='Ignore all errors when decoding.')
@click.option('--silent', 'logmsg', flag_value='silent',
              help='Suppress all progress information.')
@click.option('--debug', 'logmsg', flag_value='debug',
              help='Output debug progress information.')
@click.pass_context
def main(ctx, **kwargs):
    """Create or inspect NFC Data Exchange Format messages.

    The ndeftool provides a number of commands to create or inspect
    NDEF messages. All commands can be chained to an internal
    processing pipeline and the whole fit into a command shell
    pipeline.

    \b
      ndeftool load FILE1 load FILE2 save FILE3
      ndeftool load - load FILE2 < FILE1 > FILE3
      cat FILE1 | ndeftool load - load FILE2 | hexdump -Cv

    The ndeftool processing pipeline builds an NDEF message from left
    to right, each command adds some NDEF record(s) to the message
    until it is either send to standard output or consumed by an
    ndeftool command (unless the --keep option is given to a command
    that would otherwise consume the message).

    \b
      ndeftool text 'one' text 'two' print --keep > two_text_records.ndef
      ndeftool text 'one' text 'two' save --keep two_text_records.ndef print

    A new pipeline is started after ndeftool command that consumed the
    current message. This can be used to generate or inspect multiple
    messages.

    \b
      ndeftool text 'one' save text_1.ndef text 'two' save text_2.ndef
      ndeftool load text_1.ndef print load text_2.ndef print

    Each command has it's own help page: 'ndeftool <cmd> --help'
    """
    ctx.meta['decode-errors'] = kwargs['errors'] or 'strict'
    ctx.meta['output-logmsg'] = kwargs['logmsg'] or 'normal'


@main.resultcallback()
def process_commands(processors, **kwargs):
    message = None
    for processor in processors:
        message = processor(message)
        dmsg('records = ' + str(message))
    echo(b''.join(ndef.message_encoder(message)), nl=False)


def command_processor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def processor(message):
            return func(message, *args, **kwargs)
        return processor
    return wrapper
