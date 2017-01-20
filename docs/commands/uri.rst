.. -*- mode: rst; fill-column: 80 -*-

.. _uri:

uri
===

Create an NFC Forum URI Record.

Synopsis
--------

.. code::

   ndeftool uri [OPTIONS] RESOURCE

Description
-----------

The **uri** command creates an NFC Forum URI Record wit the given resource
identifier. Note that this is actually an Internationalized Resource Identifier
(IRI).

Options
-------

.. option:: --help

            Show this message and exit.

Examples
--------

Create a URI record that links to `http://nfcpy.org`.

.. command-output:: ndeftool uri 'http://nfcpy.org' print
