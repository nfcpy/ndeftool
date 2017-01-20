# -*- coding: utf-8 -*-

import click
import ndef

from ndeftool.cli import command_processor, dmsg


@click.command(short_help="Create an NFC Forum URI Record.")
@click.argument('resource')
@command_processor
def cmd(message, **kwargs):
    """The *uri* command creates an NFC Forum URI Record wit the given
    resource identifier. Note that this is actually an
    Internationalized Resource Identifier (IRI).

    \b
    Examples:
      ndeftool uri 'http://nfcpy.org' print

    """
    dmsg(__name__ + ' ' + str(kwargs))

    if message is None:
        message = []

    record = ndef.UriRecord(kwargs['resource'])

    message.append(record)
    return message
