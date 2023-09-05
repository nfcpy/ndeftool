=====================================
Create, modify and print NDEF Records
=====================================

.. image:: https://img.shields.io/pypi/v/ndeftool
   :target: https://pypi.python.org/pypi/ndeftool
   :alt: Python Package

.. image:: https://img.shields.io/readthedocs/ndeftool
   :target: http://ndeftool.readthedocs.io
   :alt: Documentation

.. image:: https://img.shields.io/codecov/c/github/nfcpy/ndeftool
   :target: https://codecov.io/gh/nfcpy/ndeftool
   :alt: Code Coverage

The ``ndeftool`` is a command line utility to create or inspect NFC
Data Exchange Format (NDEF) records and messages, released under the
`ISC <http://choosealicense.com/licenses/isc/>`_ license.

.. code-block:: shell

   $ ndeftool text "Hello World" id "r1" uri "http://nfcpy.org" save -k "message.ndef" print
   Saving 2 records to message.ndef.
   NDEF Text Record ID 'r1' Text 'Hello World' Language 'en' Encoding 'UTF-8'
   NDEF Uri Record ID '' Resource 'http://nfcpy.org'

The ``ndeftool`` documentation can be found on `Read the Docs
<https://ndeftool.readthedocs.io/>`_ and the code on `GitHub
<https://github.com/nfcpy/ndeftool>`_.
