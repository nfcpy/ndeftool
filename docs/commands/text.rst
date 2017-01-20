.. -*- mode: rst; fill-column: 80 -*-

.. _text:

text
====

Create an NFC Forum Text Record.

Synopsis
--------

.. code::

   ndeftool text [OPTIONS] TEXT
   ndeftool txt [OPTIONS] TEXT

Description
-----------

The **text** command creates an NFC Forum Text Record with the given input
text. The text language defaults to English (language code `en`) and can be set
with `--language` followed by the IANA language code. The text content is
encoded as UTF-8 or UTF-16 depending on `--encoding`. The default encoding is
UTF-8.

Options
-------

.. option:: -l, --language TEXT

            Set the IANA language code.

.. option:: --encoding [UTF-8|UTF-16]

            Set the encoding (default UTF-8).

.. option:: --help

            Show this message and exit.

Examples
--------

Create an NFC Forum Text Record with the default language `en` and encoding `UTF-8`.

.. command-output:: ndeftool text 'created with the nfcpy ndeftool' print

Create one text record with English text and one record with German text.

.. command-output:: ndeftool text --language en 'English' text --language de 'Deutsch' print

Create a text record with UTF-16 encoding.

.. command-output:: ndeftool text --encoding UTF-16 'text encoded in UTF-16' | hd
   :shell:
