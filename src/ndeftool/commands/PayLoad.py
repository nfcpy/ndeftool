# -*- coding: utf-8 -*-

import click
import ndef

from ndeftool.cli import command_processor, dmsg


@click.command(short_help='Change the payload of the last record.')
@click.argument('data', type=click.UNPROCESSED)
@click.option('-x', '--no-check', is_flag=True,
              help='Do not check decoding after data change.')
@command_processor
@click.pass_context
def cmd(ctx, message, **kwargs):
    """The *payload* command either changes the current last record's
    data (NDEF Record PAYLOAD) or, if the current message does
    not have any records, creates a record with the given record
    data. The changed record is verified to successfully encode and
    decode unless disabled with -x.

    The data string may contain hexadecimal bytes using '\\xNN'
    notation where each N is a nibble from [0-F].

    \b
    Examples:
      ndeftool payload 'Hello World' typename 'text/plain' print
      ndeftool payload '\\x02enHello World' typename 'urn:nfc:wkt:T' print -l

    """
    dmsg(__name__ + ' ' + str(kwargs))
    dmsg(repr(kwargs['data']))

    if not message:
        message = [ndef.Record('unknown')]

    record_type = message[-1].type
    record_name = message[-1].name
    record_data = eval(repr(kwargs['data'].encode()).replace('\\\\', '\\'))

    record = ndef.Record(record_type, record_name, record_data)

    if not kwargs['no_check']:
        octets = b''.join(ndef.message_encoder([record]))
        errors = ctx.meta['decode-errors']
        try:
            record = next(ndef.message_decoder(octets, errors))
        except ndef.DecodeError as error:
            raise click.ClickException(str(error))

    message[-1] = record
    return message
