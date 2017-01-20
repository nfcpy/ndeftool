# -*- coding: utf-8 -*-

import click
import ndef

from ndeftool.cli import command_processor, dmsg, info, echo

LONG_FORMAT = "  {:10} {}"


@click.command(short_help="Print records as human readable.")
@click.option('-l', '--long', is_flag=True, help="use a long print format")
@click.option('-k', '--keep', is_flag=True, help="keep message in pipeline")
@command_processor
@click.pass_context
def cmd(ctx, message, **kwargs):
    """The *print* command outputs a formatted representation of all
    current NDEF Records. By default this is the one line str()
    representation for each record. The '--long' format produces
    multiple indented lines per record in an attempt to provide a more
    readable output. Printing consumes all records so that no more
    data is send to stdout or given to the next command. This can be
    changed with the '--keep' flag.

    When given as the first command *print* attempts to decode an NDEF
    message from standard input and then process the generated list of
    records.

    \b
    Examples:
      ndeftool text 'made with ndeftool' print
      ndeftool text 'say one' print text 'say two' print
      ndeftool text one print --keep text two print
      ndeftool text 'print from stdin' | ndeftool print
      ndeftool text 'before' | ndeftool print text 'after' print

    """
    dmsg(__name__ + ' ' + str(kwargs))

    if message is None:
        info("Reading data from standard input")
        octets = click.get_binary_stream('stdin').read()
        errors = ctx.meta['decode-errors']
        try:
            message = list(ndef.message_decoder(octets, errors))
        except ndef.DecodeError as error:
            raise click.ClickException(str(error))

    for index, record in enumerate(message):
        if not kwargs['long']:
            echo(str(record))
            continue

        if isinstance(record, ndef.TextRecord):
            echo("NFC Forum Text Record [record #{}]".format(index+1))
            echo(LONG_FORMAT.format("content", record.text))
            echo(LONG_FORMAT.format("language", record.language))
            echo(LONG_FORMAT.format("encoding", record.encoding))
        elif isinstance(record, ndef.UriRecord):
            echo("NFC Forum URI Record [record #{}]".format(index+1))
            echo(LONG_FORMAT.format("resource", record.iri))
        elif isinstance(record, ndef.SmartposterRecord):
            echo("NFC Forum Smart Poster Record [record #{}]".format(index+1))
            echo(LONG_FORMAT.format("resource", record.resource.iri))
            if record.action:
                echo(LONG_FORMAT.format("action", record.action))
            for lang, text in record.titles.items():
                echo(LONG_FORMAT.format("title_" + lang, text))
            for icon_type, icon_data in record.icons.items():
                echo(LONG_FORMAT.format(icon_type, "%d byte" % len(icon_data)))
        else:
            echo("Record [record #{}]".format(index+1))
            echo(LONG_FORMAT.format("type", record.type))
            echo(LONG_FORMAT.format("name", record.name))
            echo(LONG_FORMAT.format("data", bytes(record.data)))

    return message if kwargs['keep'] else []
