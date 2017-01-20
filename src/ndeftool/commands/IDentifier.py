# -*- coding: utf-8 -*-

import click
import ndef

from ndeftool.cli import command_processor, dmsg


@click.command(short_help="Change the identifier of the last record.")
@click.argument('name')
@command_processor
def cmd(message, **kwargs):
    """The *identifier* command either changes the current last record's
    name (NDEF Record ID) or, if the current message does not have any
    records, creates a record with unknown record type and the given
    record name.

    \b
    Examples:
      ndeftool identifier 'record identifier' print
      ndeftool text 'first' id 'r1' text 'second' id 'r2' print

    """
    dmsg(__name__ + ' ' + str(kwargs))

    if not message:
        message = [ndef.Record('unknown')]

    try:
        message[-1].name = kwargs['name'].encode('latin', 'replace')
    except ValueError as error:
        raise click.ClickException(str(error))

    return message
