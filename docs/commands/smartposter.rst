.. -*- mode: rst; fill-column: 80 -*-

.. _smartposter:

smartposter
===========

Create an NFC Forum Smart Poster Record.

Synopsis
--------

.. code::

   ndeftool smartposter [OPTIONS] RESOURCE
   ndeftool smp [OPTIONS] RESOURCE

Description
-----------

The **smartposter** command creates an NFC Forum Smart Poster Record for the
resource identifier. A smart poster record combines the uniform resource
identifier with additional data such as titles and icons for representation and
processing instructions for the reader application.

A smart poster record should have title text for the desired languages, added
with repetitive `-t` options. An English title text may also be added with
`-T`. The recommended action set with `-a` tells the reader application to
either run the default action for the URI, save it for later or open for
editing.

A smart poster may also provide a collection of icons for graphical
representation. An icon file is added with the `-i` option that may be given
more than once. The icon type is determined from the file content and must be an
image or video mime type.

Options
-------

.. option:: -T TEXT

            Smartposter title for language code 'en'.

.. option:: -t LANG TEXT

            Smartposter title for a given language code.

.. option:: -a [exec|save|edit]

            Recommended action for handling the resource.

.. option:: -i FILENAME

            Icon file for a graphical representation.

.. option:: --help

            Show this message and exit.

Examples
--------

An NFC Forum Smart Poster Record with just a link, nothing more useful than a URI Record.

.. command-output:: ndeftool smartposter http://nfcpy.org print

Same as above but with an English title.

.. command-output:: ndeftool smartposter -T 'nfcpy project' http://nfcpy.org print

Titles for other languages must be given with a language code.

.. command-output:: ndeftool smartposter -t de 'Google Deutschland' https://www.google.de print

An emergency call number should be called immediately.

.. command-output:: ndeftool smartposter -T 'EMERGENCY CALL 911' -a exec 'tel:911' print -l

Add an icon file to a smart poster.

.. command-output:: ndeftool smp -i images/ndeftool.png https://github.com/nfcpy/ndeftool print -l
