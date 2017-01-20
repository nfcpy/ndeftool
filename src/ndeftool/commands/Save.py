# -*- coding: utf-8 -*-

import os.path
import shutil
import click
import ndef

from ndeftool.cli import command_processor, dmsg, info, warn


@click.command(short_help="Save records or payloads to disk.")
@click.argument('path', type=click.Path(writable=True))
@click.option('--skip', type=click.IntRange(min=0), default=0,
              metavar='N', help="Skip the first N records.")
@click.option('--count', type=click.IntRange(min=1), default=None,
              metavar='N', help="Skip the first N records.")
@click.option('--head', type=click.IntRange(min=1), default=None,
              metavar='N', help="Save the first N records.")
@click.option('--tail', type=click.IntRange(min=1), default=None,
              metavar='N', help="Save the last N records.")
@click.option('-b', '--burst', is_flag=True,
              help="Save single record files in directory.")
@click.option('-u', '--unpack', is_flag=True,
              help="Unpack records to files in directory.")
@click.option('-f', '--force', is_flag=True,
              help="Replace existing file or directory.")
@click.option('-k', '--keep', is_flag=True,
              help="Forward records to next command.")
@command_processor
@click.pass_context
def cmd(ctx, message, **kwargs):
    """The *save* command writes the current records to disk. The records
    to write can be restricted to the subset selected with '--skip',
    '--count', '--head' and '--tail' applied in that order. The
    default mode is to save all selected records as one NDEF message
    into a single file given by PATH. In '--burst' mode each record is
    written as one NDEF message into a separate file under the
    directory given by PATH. The file names are three digit numbers
    created from the record index. In '--unpack' mode the payload of
    each record is written to a separate file under directory PATH
    with the file name set to the record name (NDEF Record ID).
    Records without name are not written unless '--unpack' and
    '--burst' are both set.

    The *save* command does not replace existing files or directories
    unless this is requested with '--force'.

    The *save* command consumes records from the internal message
    pipe. This can be prevented with '--keep', all records are then
    forwarded to the next command or written to standard output. When
    *save* is the first command it creates the pipe by reading from
    standard input.

    \b
    Examples:
      ndeftool text 'Hello World' save text.ndef
      ndeftool text 'Hello World' | ndeftool save text.ndef
      ndeftool text 'One' save one.ndef text 'Two' save two.ndef

    """
    dmsg(__name__ + ' ' + str(kwargs))

    path = kwargs['path']

    if os.path.exists(path) and not kwargs['force']:
        errmsg = "path '%s' exists. Use '--force' to replace."
        raise click.ClickException(errmsg % path)

    if message is None:
        info("Reading data from standard input")
        octets = click.get_binary_stream('stdin').read()
        errors = ctx.meta['decode-errors']
        try:
            message = list(ndef.message_decoder(octets, errors))
        except ndef.DecodeError as error:
            raise click.ClickException(str(error))

    first = min(kwargs['skip'], len(message))
    count = min(kwargs['count'] or len(message), len(message))
    head = min(kwargs['head'] or count, count)
    tail = min(kwargs['tail'] or count, count)
    dmsg("first=%d count=%d head=%d tail=%d" % (first, count, head, tail))
    count = min(head, tail, len(message) - first)
    first = first + head - min(head, tail)
    dmsg("first=%d count=%d head=%d tail=%d" % (first, count, head, tail))

    if kwargs['burst'] or kwargs['unpack']:
        path = os.path.normpath(path)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            os.mkdir(path)
        except (OSError, IOError) as error:
            raise click.ClickException(str(error))

        for index, record in enumerate(message[first:first+count]):
            name = None
            if kwargs['unpack'] and record.name:
                name = record.name
            if kwargs['burst'] and not name:
                name = '%03d.ndef' % index
            if name:
                with click.open_file('%s/%s' % (path, name), 'wb') as f:
                    info("Saving 1 record to {}.".format(f.name))
                    if kwargs['unpack']:
                        f.write(record.data)
                    else:
                        f.write(b''.join(ndef.message_encoder([record])))
            else:
                warn("Skipping 1 record without name")
    else:
        with click.open_file(path, 'wb') as f:
            filename = f.name if f.name != '-' else '<stdout>'

            info("Saving {num} record{s} to {path}.".format(
                num=count, path=filename, s=('', 's')[count > 1]))

            f.write(b''.join(ndef.message_encoder(message[first:first+count])))

    if not kwargs['keep']:
        del message[first:first+count]

    return message
