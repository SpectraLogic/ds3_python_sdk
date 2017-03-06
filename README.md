Generating the DS3 Python SDK Documentation
===========================================

The Python SDK documentation is built using [Sphinx](http://sphinx-doc.org/).

To install sphinx on Ubuntu, run the following command:

    $ sudo apt-get install python-sphinx

The Python documentation is on the branch gh-pages (Github hosted sites need to be on a branch named gh-pages,
so any changes to the documentation need to be on this branch, not master). Pull from this branch, and you should see an
a directory called sphinx in the repository. This directory is where all the documentation actually lives.

Sphinx generates it's documentation from installed modules, so before generating documentation,
make sure the ds3.ds3 Python module is installed.

To install the ds3.ds3 module, run

    $ sudo python setup.py install
    
Generating documentation
------------------------

To (re)generate the documentation, navigate to the directory the documentation is in,
"repository"/sphinx/"version you want to generate" (currently v1.0-0), and run

    $ sphinx-build -b html source/ .


Adding a new version or release
-------------------------------

To add a new version of the documentation, navigate to the sphinx directory and copy one of the existing directories into
a new directory corresponding to the version and release you want. In the new directory, edit the variables 'source' and
'release' in the file <new directory>/source/conf.py to match the new version and release numbers. Run

    $ sphinx-build -b html source/ .
