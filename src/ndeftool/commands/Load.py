# -*- coding: utf-8 -*-

import click
import magic
import glob
import ndef

from ndeftool.cli import command_processor, info, warn, dmsg


@click.command(short_help="Load records or payloads from disk.")
@click.argument('path', type=click.Path())
@click.option('-p', '--pack', is_flag=True,
              help="Pack files as payload into mimetype records.")
@command_processor
@click.pass_context
def cmd(ctx, message, **kwargs):
    """The *load* command reads records or payloads from disk files or
    standard input. The files to read are searched with the pattern
    specified by PATH which in the simplest form is an existing file
    name. Other forms may include '*', '?' and character ranges
    expressed by '[]'. A single '-' may be used to read from standard
    input. Note that patterns containg wildcards may need to be
    escaped to avoid shell expansion.

    The default mode of operation is to load files containing NDEF
    records. In '--pack' mode the files are loaded into the payload of
    NDEF records with record type (NDEF Record TNF and TYPE) set to
    the mimetype discovered from the payload and record name (NDEF
    Record ID) set to the filename.

    \b
    Examples:
      ndeftool load message.ndef print
      ndeftool load '*.ndef' print
      cat message.ndef | ndeftool load - print
      ndeftool load --pack /etc/hostname print
      ndeftool load --pack '/etc/cron.daily/*' print

    """
    dmsg(__name__ + ' ' + str(kwargs))

    if message is None:
        message = []

    if kwargs['path'] == '-':
        filenames = kwargs['path']
    else:
        filenames = sorted(glob.iglob(kwargs['path']))

    if len(filenames) == 0:
        info("No files selected by path '%s'." % kwargs['path'])

    for filename in filenames:
        try:
            f = click.open_file(filename, 'rb')
        except (OSError, IOError) as error:
            warn(str(error))
        else:
            if kwargs['pack']:
                message.append(pack_file(f))
            else:
                message.extend(load_file(f, ctx.meta['decode-errors']))

    return message


def pack_file(f):
    record_data = f.read()
    record_type = magic.from_buffer(record_data, mime=1)
    record_name = getattr(f, 'name', '<stdin>')[0:255]
    return ndef.Record(record_type, record_name, record_data)


def load_file(f, decode_errors):
    fn = getattr(f, 'name', '<stdin>')
    try:
        records = list(ndef.message_decoder(f.read(), decode_errors))
        info("loaded %d record(s) from %s" % (len(records), fn))
        return records
    except ndef.DecodeError as error:
        dmsg(str(error))
        errmsg = "%s does not contain a valid NDEF message." % fn
        raise click.ClickException(errmsg)
