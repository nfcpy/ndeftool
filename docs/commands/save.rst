.. -*- mode: rst; fill-column: 80 -*-

.. _save:

save
====

Save records or payloads to disk.

Synopsis
--------

.. code::

   ndeftool save [OPTIONS] PATH
   ndeftool s [OPTIONS] PATH

Description
-----------

The **save** command writes the current records to disk. The records to write
can be restricted to the subset selected with `--skip`, `--count`, `--head` and
`--tail` applied in that order. The default mode is to save all selected records
as one NDEF message into a single file given by PATH.  In `--burst` mode each
record is written as one NDEF message into a separate file under the directory
given by PATH. The file names are three digit numbers created from the record
index. In `--unpack` mode the payload of each record is written to a separate
file under directory PATH with the file name set to the record name (NDEF Record
ID). Records without name are not written unless `--unpack` and `--burst` are
both set.

The **save** command does not replace existing files or directories unless this is
requested with `--force`.

The **save** command consumes records from the internal message pipe. This can
be prevented with `--keep`, all records are then forwarded to the next command
or written to standard output. When **save** is the first command it creates the
pipe by reading from standard input.

Options
-------

.. option:: --skip N

            Skip the first N records.

.. option:: --count N

            Skip the first N records.

.. option:: --head N

            Save the first N records.

.. option:: --tail N

            Save the last N records.

.. option:: -b, --burst

            Save single record files in directory.

.. option:: -u, --unpack

            Unpack records to files in directory.

.. option:: -f, --force

            Replace existing file or directory.

.. option:: -k, --keep

            Forward records to next command.

.. option:: --help

            Show this message and exit.

Examples
--------

Create an NFC Forum Text Record and save it to to a file in the /tmp directory,
overwriting the file if it exists.

.. command-output:: ndeftool text "Hello World" save --force /tmp/hello.ndef

Same as above but the with three NDEF Text Records.

.. command-output:: ndeftool text One text Two text Three save --force /tmp/text.ndef

Out of three records the second is saved using the `--skip` and `--count`
options and the others are forwarded to print.

.. command-output:: ndeftool txt aa txt bb txt cc save -f --skip 1 --count 1 /tmp/text.ndef print

Out of three records the second is saved using the `--head` and `--tail` options
and the others are forwarded to print.

.. command-output:: ndeftool txt aa txt bb txt cc save -f --head 2 --tail 1 /tmp/text.ndef print

Save each record to a separate file with auto-numbered file name plus `.ndef`
extension.

.. command-output:: ndeftool txt aa txt bb txt cc save -f --burst /tmp/text/

Unpack record payloads to separate files using the record identifier as the file
name.

.. command-output:: ndeftool txt aa id 1.txt txt bb id 2.txt txt cc id 3.txt save -f --unpack /tmp/text/
