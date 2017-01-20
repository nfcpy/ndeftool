.. -*- mode: rst; fill-column: 80 -*-

.. _typename:

typename
========

Change the type name of the last record.

Synopsis
--------

.. code::

   ndeftool typename [OPTIONS] TYPE
   ndeftool tn [OPTIONS] TYPE

Description
-----------

The **typename** command either changes the current last record's type (NDEF
Record TNF and TYPE) or, if the current message does not have any records,
creates a record with the given record type. The changed record is verified to
successfully encode and decode unless disabled with `-x`.

Options
-------

.. option:: -x, --no-check

            Do not check decoding after type name change.

.. option:: --help

            Show this message and exit.

Examples
--------

Create a record with `text/plain` mime type and no payload.

.. command-output:: ndeftool typename 'text/plain' print

Create a plain text record and add some payload.

.. command-output:: ndeftool typename 'text/plain' payload 'Hello World' print

Create a record with a payload that does not match the record type.

.. command-output:: ndeftool payload 'Hello World' typename -x 'urn:nfc:wkt:T' print -l
