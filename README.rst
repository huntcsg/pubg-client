pubg-client
-----------

**A python client for the pubg API**

|travis| |pypi| |docs|

Features:

    * Versioned API Endpoint and response payloads
    * Pagination Support


    .. DANGER::

       This library is in alpha. I will try my utmost to not make backwards incompatible changes
       but it is possible that they will be necessary.

Installing
==========

   .. code-block:: shell

      $ pip install pubg-client

Development
===========

   .. code-block:: shell

      $ git clone https://github.com/huntcsg/pubg-client.git
      $ cd pubg-client
      $ ./utils/manage clean
      $ ./utils/manage test
      $ ./utils/manage docs


1. All pull requests must pass the travis-ci builds
2. All pull requests should include inline (docstring) documentation, updates to built documentation if applicable,
   and test coverage. This project aspires to be a 100% test coverage library.


.. |travis| image:: https://travis-ci.org/huntcsg/pubg-client.svg?branch=master
   :target: https://travis-ci.org/huntcsg/pubg-client
.. |pypi| image:: https://img.shields.io/pypi/v/pubg-client.svg
   :target: https://pypi.python.org/pypi/pubg-client
.. |docs| image:: https://readthedocs.org/projects/pubg-client/badge/?version=latest
   :target: http://pubg-client.readthedocs.io/en/latest/?badge=latest