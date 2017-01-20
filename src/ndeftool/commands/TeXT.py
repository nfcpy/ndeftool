# -*- coding: utf-8 -*-

import click
import ndef

from ndeftool.cli import command_processor, dmsg


@click.command(short_help="Create an NFC Forum Text Record.")
@click.argument('text')
@click.option('-l', '--language', default='en',
              help="Set the IANA language code.")
@click.option('--encoding', default='UTF-8',
              type=click.Choice(['UTF-8', 'UTF-16']),
              help="Set the encoding (default UTF-8).")
@command_processor
def cmd(message, **kwargs):
    """The *text* command creates an NFC Forum Text Record with the given
    input text. The text language defaults to 'en' and can be set
    with --language followed by the IANA language code.

    \b
    Examples:
      ndeftool text '' | hexdump -Cv
      ndeftool text 'Created with the nfcpy ndeftool.' print
      ndeftool text 'first record' text 'second record' print
      ndeftool text -l en 'English' text -l de 'Deutsch' print

    """
    dmsg(__name__ + ' ' + str(kwargs))

    if message is None:
        message = []

    content = kwargs['text']
    language = kwargs['language']
    encoding = kwargs['encoding']

    record = ndef.TextRecord(content, language, encoding)

    message.append(record)
    return message
