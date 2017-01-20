.. -*- mode: rst; fill-column: 80 -*-

.. print:

print
=====

Print records as human readable.

Synopsis
--------

.. code::

   ndeftool print [OPTIONS]
   ndeftool p [OPTIONS]

Description
-----------

The **print** command outputs a formatted representation of all current NDEF
Records. By default this is the one line str() representation for each
record. The `--long` format produces multiple indented lines per record in an
attempt to provide a more readable output. Printing consumes all records so that
no more data is send to stdout or given to the next command. This can be changed
with the `--keep` flag.

When given as the first command **print** attempts to decode an NDEF message
from standard input and process the generated list of records.

Options
-------

.. option:: -l, --long

            Output in a long print format.

.. option:: -k, --keep

            Keep records for next command.

.. option:: --help

            Show this message and exit.

Examples
--------

Print records in short format.

.. command-output:: ndeftool text "Hello World" print

Print records in long format.

.. command-output:: ndeftool text "Hello World" print --long

Print records in both short and long format.

.. command-output:: ndeftool text "Hello World" print --keep print --long
