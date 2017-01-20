.. -*- mode: rst; fill-column: 80 -*-

.. _identifier:

identifier
==========

Change the identifier of the last record.

Synopsis
--------

.. code::

   ndeftool identifier [OPTIONS] NAME
   ndeftool id [OPTIONS] NAME

Description
-----------

The **identifier** command either changes the current last record's name (NDEF
Record ID) or, if the current message does not have any records, creates a
record with unknown record type and the given record name.

Options
-------

.. option:: --help

            Show this message and exit.

Examples
--------

Create a record with `unknown` type and set the identifier.

.. command-output:: ndeftool identifier 'record identifier' print

Create two text records with specific identifiers.

.. command-output:: ndeftool text 'first' id 'r1' text 'second' id 'r2' print

