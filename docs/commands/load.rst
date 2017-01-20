.. -*- mode: rst; fill-column: 80 -*-

.. _load:

load
====

Load records or payloads from disk.

Synopsis
--------

.. code::

   ndeftool load [OPTIONS] PATH
   ndeftool l [OPTIONS] PATH

Description
-----------

The **load** command reads records or payloads from disk files or
standard input. The files for reading are determined by the pattern
specified by PATH, which in the simplest form is an existing file
name. Other forms may include `*`, `?` and character ranges expressed
by `[]`. A single `-` may be used to read from standard input. Note
that patterns containg wildcards may need to be escaped to avoid shell
expansion.

The default mode of operation is to load files containing NDEF
records. In `--pack` mode the files are loaded into the payload of
NDEF records with record type (NDEF Record TNF and TYPE) set to the
mimetype discovered from the payload and record name (NDEF Record ID)
set to the filename.

Options
-------

.. option:: -p, --pack

   Pack files as payload into mimetype records.

.. option:: --help

   Show this message and exit.

Examples
--------

Pack text from standard input and pack as record.

.. command-output:: echo -n "Hello World" | ndeftool load --pack - print
   :shell:

Read text from file and pack as record.

.. command-output:: echo -n "Hello World" > /tmp/hello && ndeftool load --pack /tmp/hello print
   :shell:

Read with path containing wildcard characters.

.. command-output:: ndeftool load --pack 'i?d*.rst' print

Read and pack multiple files.

.. command-output:: ndeftool load --pack '../se?up.*' print
