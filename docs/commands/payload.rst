.. -*- mode: rst; fill-column: 80 -*-

.. _payload:

payload
=======

Change the payload of the last record.

Synopsis
--------

.. code::

   ndeftool payload [OPTIONS] DATA
   ndeftool pl [OPTIONS] DATA

Description
-----------

The **payload** command either changes the current last record's data (NDEF
Record PAYLOAD) or, if the current message does not have any records, creates a
record with the given record data. The changed record is verified to
successfully encode and decode unless disabled with `-x`.

The data string may contain hexadecimal bytes using `\xNN` notation where
each N is a nibble from [0-F].

Options
-------

.. option:: -x, --no-check

            Do not check decoding after type name change.

.. option:: --help

            Show this message and exit.

Examples
--------

Create a plain text payload record.

.. command-output:: ndeftool payload 'Hello World' typename 'text/plain' print

Create an NFC Forum Text record with language code and content.

.. command-output:: ndeftool payload '\x02enHello World' typename 'urn:nfc:wkt:T' print -l

Create a record with a payload that does not match the record type. The first
command creates an NFC Forum Text Record with language code identifier and text
content. The second command then replaces the payload with just the text and
would make decoding fail.

.. command-output:: ndeftool text 'Hello World' payload -x 'Hello World' print -l
