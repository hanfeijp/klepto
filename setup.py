#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu

from __future__ import with_statement, absolute_import
import os

# set version numbers
stable_version = '0.0a1'
target_version = '0.1a1'
is_release = False

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# generate version number
if os.path.exists('klepto/info.py'):
    # is a source distribution, so use existing version
    os.chdir('klepto')
    with open('info.py','r') as f:
        f.readline() # header
        this_version = f.readline().split()[-1].strip("'")
    os.chdir('..')
elif stable_version == target_version:
    # we are building a stable release
    this_version = target_version
else:
    # we are building a distribution
    this_version = target_version + '.dev'
    if is_release:
        from datetime import date
        today = "".join(date.isoformat(date.today()).split('-'))
        this_version += "-" + today

# get the license info
with open('LICENSE') as file:
    license_text = file.read()

# generate the readme text
long_description = \
"""---------------------------------------------------
klepto: a utility for caching and archiving
---------------------------------------------------

Klepto extends python's 'lru_cache' to utilize different keymaps and
alternate caching algorithms, such as 'lfu_cache' and 'mru_cache'.
While caching is meant for fast access to saved results, klepto also
has archiving capabilities, for longer-term storage. Klepto uses a
simple dictionary-sytle interface for all caches and archives, and all
caches can be applied to any python function as a decorator. Keymaps
are algorithms for converting a function's input signature to a unique
dictionary, where the function's results are the dictionary value.
Thus for y = f(x), y will be stored in cache[x] (e.g. {x:y}).

Klepto provides both standard and 'safe' caching, where safe caches
are slower but can recover from hashing errors. Klepto is intended
to be used for distributed and parallel computing, where several of
the keymaps serialize the stored objects. Caches and archives are
intended to be read/write accessible from different threads and
processes. Klepto enables a user to decorate a function, save the
results to a file or database archive, close the interpreter,
start a new session, and reload the function and it's cache.

Klepto is part of pathos, a python framework for heterogenous computing.
Klepto is in the early development stages, and any user feedback is
highly appreciated. Contact Mike McKerns [mmckerns at caltech dot edu]
with comments, suggestions, and any bugs you may find. A list of known
issues is maintained at http://dev.danse.us/trac/pathos/query.


Major Features
==============

Klepto has standard and 'safe' variants of the following::

    - 'lfu_cache' - the least-frequently-used caching algorithm
    - 'lru_cache' - the least-recently-used caching algorithm
    - 'mru_cache' - the most-recently-used caching algorithm
    - 'rr_cache' - the random-replacement caching algorithm
    - 'no_cache' - a dummy caching interface to archiving
    - 'inf_cache' - an infinitely-growing cache

Klepto has the following archive types::

    - 'file_archive' - a dictionary-style interface to a file
    - 'db_archive' - a dictionary-style interface to a database
    - 'null_archive' - a dictionary-style interface to a dummy archive 

Klepto provides the following keymaps::

    - 'keymap' - keys are raw python objects
    - 'hashmap' - keys are the hash for the python object
    - 'stringmap' - keys are the __repr__ for the python object
    - 'picklemap' - keys are the serialized python object

Klepto also includes a few useful decorators providing::

    - simple, shallow, or deep rounding


Current Release
===============

This release version is klepto-%(relver)s. You can download it here.
The latest released version of klepto is always available from::

    http://dev.danse.us/trac/pathos

Klepto is distributed under a 3-clause BSD license.


Development Release
===================

You can get the latest development release with all the shiny new features at::

    http://dev.danse.us/packages

or even better, fork us on our github mirror of the svn trunk::

    https://github.com/uqfoundation


Installation
============

Klepto is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf klepto-%(thisver)s.tgz
    $ cd klepto-%(thisver)s
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings
after you run the "build" step above. 

Alternately, klepto can be installed with easy_install or pip::

    [download]
    $ easy_install -f . klepto


Requirements
============

Klepto requires::

    - python2, version >= 2.5  *or*  python3, version >= 3.1
    - dill, version >= 0.2b2.dev

Optional requirements::

    - setuptools, version >= 0.6


Usage Notes
===========

Probably the best way to get started is to look at the tests
that are provide within klepto. See `klepto.tests` for a set of scripts
that test klepto's caching and archiving functionalities. Klepto's
source code is also generally well documented, so further questions may
be resolved by inspecting the code itself.


License
=======

Klepto is distributed under a 3-clause BSD license.

    >>> import klepto
    >>> print (klepto.license())


Citation
========

If you use klepto to do research that leads to publication,
we ask that you acknowledge use of klepto by citing the
following in your publication::

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://dev.danse.us/trac/pathos


More Information
================

Please see http://dev.danse.us/trac/pathos for further information.

""" % {'relver' : stable_version, 'thisver' : this_version}

# write readme file
with open('README', 'w') as file:
    file.write(long_description)

# generate 'info' file contents
def write_info_py(filename='klepto/info.py'):
    contents = """# THIS FILE GENERATED FROM SETUP.PY
this_version = '%(this_version)s'
stable_version = '%(stable_version)s'
readme = '''%(long_description)s'''
license = '''%(license_text)s'''
"""
    with open(filename, 'w') as file:
        file.write(contents % {'this_version' : this_version,
                               'stable_version' : stable_version,
                               'long_description' : long_description,
                               'license_text' : license_text })
    return

# write info file
write_info_py()

# build the 'setup' call
setup_code = """
setup(name='klepto',
      version='%s',
      description='a utility for caching and archiving',
      long_description = '''%s''',
      author = 'Mike McKerns',
      maintainer = 'Mike McKerns',
      maintainer_email = 'mmckerns@caltech.edu',
      license = 'BSD',
      platforms = ['any'],
      url = 'http://www.cacr.caltech.edu/~mmckerns',
      classifiers = ('Intended Audience :: Developers',
                     'Programming Language :: Python',
                     'Topic :: Physics Programming'),

      packages = ['klepto'],
      package_dir = {'klepto':'klepto'},
""" % (target_version, long_description)

# add dependencies
dill_version = '>=0.2b2.dev'
import sys
if has_setuptools:
    setup_code += """
      zip_safe=False,
      dependency_links = ['http://dev.danse.us/packages/'],
      install_requires = ['dill%s'],
""" % (dill_version)

# add the scripts, and close 'setup' call
setup_code += """
      )
"""

# exec the 'setup' code
exec(setup_code)

# if dependencies are missing, print a warning
try:
    import dill
except ImportError:
    print ("\n***********************************************************")
    print ("WARNING: One of the following dependencies is unresolved:")
    print ("    dill %s" % dill_version)
    print ("***********************************************************\n")


if __name__=='__main__':
    pass

# end of file
