# -*- coding: utf-8 -*-

import click
import ndef

from ndeftool.cli import command_processor, dmsg


@click.command(short_help='Change the type name of the last record.')
@click.argument('type')
@click.option('-x', '--no-check', is_flag=True,
              help='Do not check decoding after type name change.')
@command_processor
@click.pass_context
def cmd(ctx, message, **kwargs):
    """The *typename* command either changes the current last record's
    type (NDEF Record TNF and TYPE) or, if the current message does
    not have any records, creates a record with the given record
    type. The changed record is verified to successfully encode and
    decode unless disabled with -x.

    \b
    Examples:
      ndeftool typename 'text/plain' print
      ndeftool typename 'text/plain' payload 'Hello World' print

    """
    dmsg(__name__ + ' ' + str(kwargs))

    if not message:
        message = [ndef.Record()]

    record_type = kwargs['type'].encode('latin', 'replace')
    record_name = message[-1].name
    record_data = message[-1].data

    try:
        record = ndef.Record(record_type, record_name, record_data)
    except ValueError as error:
        raise click.ClickException(str(error))

    if not kwargs['no_check']:
        octets = b''.join(ndef.message_encoder([record]))
        errors = ctx.meta['decode-errors']
        try:
            record = next(ndef.message_decoder(octets, errors))
        except ndef.DecodeError as error:
            raise click.ClickException(str(error))

    message[-1] = record
    return message
