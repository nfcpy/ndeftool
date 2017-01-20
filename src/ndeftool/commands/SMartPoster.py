# -*- coding: utf-8 -*-

import magic
import click
import ndef

from ndeftool.cli import command_processor, dmsg


@click.command(short_help='Create an NFC Forum Smart Poster record.')
@click.argument('resource')
@click.option('-T', 'title',
              help='Smartposter title for language code \'en\'.')
@click.option('-t', 'titles', nargs=2, multiple=True, metavar='LANG TEXT',
              help='Smartposter title for a given language code.')
@click.option('-a', 'action', type=click.Choice(['exec', 'save', 'edit']),
              help='Recommended action for handling the resource.')
@click.option('-i', 'icons', multiple=True, type=click.File('rb', lazy=True),
              help='Icon file for a graphical representation.')
@command_processor
def cmd(message, **kwargs):
    """The *smartposter* command creates an NFC Forum Smart Poster Record
    for the resource identifier. A smart poster record combines the
    uniform resource identifier with additional data such as titles
    and icons for representation and processing instructions for the
    reader application.

    A smart poster should have title text entries for the desired
    languages, added with repetitive '-t' options. An English title
    text may also be added with '-T'. The recommended action set with
    '-a' tells the reader application to either run the default action
    for the URI, save it for later or open for editing.

    A smart poster may also provide a collection of icons for
    graphical representation. An icon file is added with the '-i'
    option which may be used more than once. The icon type is
    determined from the file content and must be an 'image' or 'video'
    mime type.

    \b
    Examples:
      ndeftool smartposter http://nfcpy.org print
      ndeftool smartposter -T 'nfcpy project' http://nfcpy.org print
      ndeftool smartposter -t en 'nfcpy project' http://nfcpy.org print
      ndeftool smartposter -T 'EMERGENCY CALL 911' -a exec tel:911
      ndeftool smartposter -i nfcpy-logo-32x32.ico http://nfcpy.org

    """
    dmsg(__name__ + ' ' + str(kwargs))

    if message is None:
        message = []

    record = ndef.SmartposterRecord(kwargs['resource'])
    for lang, text in kwargs['titles']:
        record.set_title(text, lang)
    if kwargs['title']:
        record.set_title(kwargs['title'], 'en')
    if kwargs['action']:
        record.action = kwargs['action']
    for icon_file in kwargs['icons']:
        icon_data = icon_file.read()
        icon_type = magic.from_buffer(icon_data, mime=True)
        if icon_type.startswith('image/') or icon_type.startswith('video/'):
            record.add_icon(icon_type, icon_data)
        else:
            errmsg = "file %s is not a proper icon file" % icon_file.name
            raise click.ClickException(errmsg)

    message.append(record)
    return message
