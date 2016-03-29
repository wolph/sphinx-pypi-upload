.. image:: https://travis-ci.org/WoLpH/sphinx-pypi-upload.svg?branch=master
    :target: https://travis-ci.org/WoLpH/sphinx-pypi-upload

Sphinx-PyPI-upload
==================

This package contains a `setuptools`_ command for uploading `Sphinx`_
documentation to the `Python Package Index`_ (PyPI) at the dedicated URL
packages.python.org. It was forked from the similarly named script from Jannis
Leidel which has not been updated since 2009.

Homepage: https://github.com/WoLpH/sphinx-pypi-upload

.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _Sphinx: http://sphinx.pocoo.org/
.. _`Python Package Index`: http://pypi.python.org/


The ``upload_sphinx`` command
------------------------------

``upload_sphinx`` will create the necessary zip file out of an arbitrary 
documentation directory and posts it to the correct URL.

It's also loosely based on Sphinx' own setuptools command build_sphinx_
which allows to easily build documentation from the command line.

The ``upload_sphinx`` command has the following options:

- ``--repository (-r)``:
  url of repository [default: http://pypi.python.org/pypi]

- ``--show-response``:
  display full response text from server

- ``--upload-dir``:
  directory to upload

.. _build_sphinx: http://bitbucket.org/birkenfeld/sphinx/src/tip/sphinx/setup_command.py

Example
--------

Assuming there is an ``Example`` package with Sphinx documentation to be
uploaded to http://packages.python.org, with the following structure::

  Example/
  |-- example.py
  |-- setup.cfg
  |-- setup.py
  |-- docs
  |   |-- build
  |   |   `-- html
  |   |-- conf.py
  |   |-- index.txt
  |   `-- tips_tricks.txt

As with any other setuptools based command, you can define useful defaults in
the setup.cfg of your Python package. The following snippet shows how to set
the option defaults of the ``build_sphinx`` and ``upload_sphinx`` setup.py 
commands::

  [build_sphinx]
  source-dir = docs/
  build-dir  = docs/build
  all_files  = 1

  [upload_sphinx]
  upload-dir = docs/build/html

To build and upload the Sphinx documentation you are now able to run::

  $ python setup.py build_sphinx
  $ python setup.py upload_sphinx

Alternatively, you can of course just pass the appropriate options directly
to the commands::

  $ python setup.py build_sphinx --source-dir=docs/ --build-dir=docs/build --all-files
  $ python setup.y upload_sphinx --upload-dir=docs/build/html
