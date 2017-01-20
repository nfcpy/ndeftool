.. -*- mode: rst; fill-column: 80 -*-

========
NDEFTOOL
========

Create, modify or print NFC Data Exchange Format Records.

Synopsis
--------

.. code::

   ndeftool [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Description
-----------

The **ndeftool** provides a number of commands to create, modify or print NDEF
records. Commands can be chained together to successively extend or modify the
list of records that are generated. Except for **save** and **print**, all
records forwarded by the last command are send to standard output as binary NDEF
message data. The **save** and **print** commands implicitly consume all records
unless the `--keep` option is set. They also, unlike all other commands, do not
start an empty record list but read from standard input when given as the first
command (the same behavior can be achieved for the **load** command by setting
the file path to `-`).

By default, NDEF records read from disk or standard input must be correctly
formatted NDEF message data (for example, the first and the last record must
have the message begin and end flag set). The `--relax` makes the decoder accept
correctable data errors and the `--ignore` option will additionally skip records
with uncorrectable errors.


Options
-------

.. option:: --version

            Show the version and exit.

.. option:: --relax

            Ignore some errors when decoding.

.. option:: --ignore

            Ignore all errors when decoding.

.. option:: --silent

            Suppress all progress information.

.. option:: --debug

            Output debug progress information.

.. option:: --help

            Show this message and exit.


Commands
--------

.. toctree::
   :maxdepth: 1

   commands/load
   commands/save
   commands/print

   commands/identifier
   commands/typename
   commands/payload

   commands/text
   commands/uri
   commands/smartposter


Examples
--------

Any NDEF Record can be constructed with the :ref:`payload`, :ref:`typename` and
:ref:`identifier` commands.

.. command-output:: ndeftool payload '\02ensample text' typename 'urn:nfc:wkt:T' id 'r1' print

The same record can be created with the :ref:`text` command. Here the output
goes to stdout and is then printed with a separate ndeftool process call.

.. command-output:: ndeftool text 'sample text' id 'r1' | ndeftool print
   :shell:

The :ref:`save` command writes the records to disk or <stdout> for path name
`-`. The following example creates an NDEF message with three NFC Forum Text
Records, the first and last record with the message begin and message end flags
set.

.. command-output:: ndeftool text ONE text TWO text THREE save - | hd
   :shell:

The :ref:`save` command can be used to write intermediate results, here
immediately after a text record has been created. Note that by writing to
<stdout> the result is a sequence of three individual NDEF messages of one
record each. This would not be a proper NDEF message file.

.. command-output:: ndeftool text ONE save - text TWO save - text THREE save - | hd
   :shell:

The :ref:`load` command reads records from disk or <stdin> for path name `-`.

.. command-output:: ndeftool text ONE text TWO text THREE | ndeftool load - print
   :shell:

An empty NDEF Record can be created with an empty type name string. The first
octet ``11010000b`` sets the Message Begin (MB) and Message End (ME) flags in
the two most signifant bits. The Type Name Format (TNF) value 0 in the least
significant three bits indicates that there is no type or payload associated
with this record and thus the `TYPE LENGTH` and `PAYLOAD LENGTH` fields must be
zero.

.. command-output:: ndeftool typename '' | hd
   :shell:

The default decoding of an NDEF message requires correct data format. Data with
minor format errors can be decoded with the `--relax` option. The following
example creates two empty records with invalid MB and ME flags that do only
decode with `--relax`.

.. command-output:: python3 -c "import sys; sys.stdout.buffer.write(b'\x10\0\0\x10\0\0')" | ndeftool --relax print
   :shell:

NDEF message data with uncorrectable errors can be skipped with the `--ignore`
option. The payload length 1 in the second record is an invalid value for an
empty record.

.. command-output:: python3 -c "import sys; sys.stdout.buffer.write(b'\x10\0\0\x10\1\0')" | ndeftool --ignore print
   :shell:
