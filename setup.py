#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu

from __future__ import with_statement
import os

# set version numbers
stable_version = '0.1a1'
target_version = '0.2a'
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
if os.path.exists('pathos/info.py'):
    # is a source distribution, so use existing version
    from pathos.info import this_version
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
"""-----------------------------------------------
pathos: a framework for heterogeneous computing
-----------------------------------------------

Pathos is a framework for heterogenous computing. It primarily provides
the communication mechanisms for configuring and launching parallel
computations across heterogenous resources. Pathos provides stagers and
launchers for parallel and distributed computing, where each launcher
contains the syntactic logic to configure and launch jobs in an execution
environment.  Some examples of included launchers are: a queue-less
MPI-based launcher, a ssh-based launcher, and a multiprocessing launcher.
Pathos also provides a map-reduce algorithm for each of the available
launchers, thus greatly lowering the barrier for users to extend their
code to parallel and distributed resources.  Pathos provides the ability
to interact with batch schedulers and queuing systems, thus allowing large
computations to be easily launched on high-performance computing resources.
One of the most powerful features of pathos is  "tunnel", which enables a
user to automatically wrap any distributed service calls within a ssh-tunnel.

Pathos is divided into four subpackages::

    - dill: a utility for serialization of python objects
    - pox: utilities for filesystem exploration and automated builds
    - pyina: a MPI-based parallel mapper and launcher
    - pathos: distributed parallel map-reduce and ssh communication


Pathos Subpackage 
=================

The pathos subpackage provides a few basic tools to make distributed
computing more accessable to the end user. The goal of pathos is to
allow the user to extend their own code to distributed computing with
minimal refactoring.

Pathos provides methods for configuring, launching, monitoring, and
controlling a service on a remote host. One of the most basic features
of pathos is the ability to configure and launch a RPC-based service
on a remote host. Pathos seeds the remote host with a small `portpicker`
script, which allows the remote host to inform the localhost of a port
that is available for communication.

Beyond the ability to establish a RPC service, and then post requests,
is the ability to launch code in parallel. Unlike parallel computing
performed at the node level (typically with MPI), pathos enables the
user to launch jobs in parallel across heterogeneous distributed resources.
Pathos provides a distributed map-reduce algorithm, where a mix of
local processors and distributed RPC services can be selected.  Pathos
also provides a very basic automated load balancing service, as well as
the ability for the user to directly select the resources.

The high-level "pp_map" interface, yields a map-reduce implementation that
hides the RPC internals from the user. With pp_map, the user can launch
their code in parallel, and as a distributed service, using standard python
and without writing a line of server or parallel batch code.

RPC servers and communication in general is known to be insecure.  However,
instead of attempting to make the RPC communication itself secure, pathos
provides the ability to automatically wrap any distributes service or
communication in a ssh-tunnel. Ssh is a universally trusted method.
Using ssh-tunnels, pathos has launched several distributed calculations
on national lab clusters, and to date has performed test calculations
that utilize node-to-node communication between two national lab clusters
and a user's laptop.  Pathos allows the user to configure and launch
at a very atomistic level, through raw access to ssh and scp. 

Pathos is in the early development stages, and any user feedback is
highly appreciated. Contact Mike McKerns [mmckerns at caltech dot edu]
with comments, suggestions, and any bugs you may find. A list of known
issues is maintained at http://dev.danse.us/trac/pathos/query.


Major Features
==============

Pathos provides a configurable distributed parallel-map reduce interface
to launching RPC service calls, with::

    - a map-reduce interface that extends the python 'map' standard
    - the ability to submit service requests to a selection of servers
    - the ability to tunnel server communications with ssh
    - automated load-balancing between multiprocessing and RPC servers

The pathos core is built on low-level communication to remote hosts using
ssh. The interface to ssh, scp, and ssh-tunneled connections can::

    - configure and launch remote processes with ssh
    - configure and copy file objects with scp
    - establish an tear-down a ssh-tunnel

To get up and running quickly, pathos also provides infrastructure to::

    - easily establish a ssh-tunneled connection to a RPC server


Current Release
===============

The latest stable release version is pathos-%(relver)s. You can download it here.
The latest stable version of pathos is always available at:

    http://dev.danse.us/trac/pathos


Development Release
===================

If you like living on the edge, and don't mind the promise
of a little instability, you can get the latest development
release with all the shiny new features at:

    http://dev.danse.us/packages.


Installation
============

Pathos is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf pathos-%(thisver)s.tgz
    $ cd pathos-%(thisver)s
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings after
you run the "build" step above. Pathos depends on dill, pox, and pyina,
each of which are essentially subpackages of pathos that are also
released independently. Pathos also depends on slightly modified
versions of `pyre` and `parallel python`; these packages are included
in the `pathos.external` directory.  The aforementioned pathos
subpackages are also available on this site, and you must install all of
the dependencies for pathos to have full functionality for heterogeneous
computing. Currently, pyina is optional.

Alternately, pathos can be installed with easy_install::

    [download]
    $ easy_install -f . pathos


Requirements
============

Pathos requires::

    - python, version >= 2.5, version < 3.0
    - dill, version >= 0.2a.dev
    - pox, version >= 0.2a.dev
    - pyre, version == 0.8-pathos (*)
    - pp, version == 1.5.7-pathos (*)

Optional requirements::

    - setuptools, version >= 0.6
    - pyina, version >= 0.2a.dev
    - rpyc, version >= 3.0.6


Usage Notes
===========

Probably the best way to get started is to look at a few of the
examples provided within pathos. See `pathos.examples` for a
set of scripts that demonstrate the configuration and launching of
communications with ssh and scp.

Important classes and functions are found here::

    - pathos.pathos.pp_map          [the map-reduce API definition]
    - pathos.pathos.core            [the high-level command interface] 
    - pathos.pathos.hosts           [the hostname registry interface] 
    - pathos.pathos.Launcher        [the launcher base class]
    - pathos.pathos.Tunnel          [the tunnel base class]

Pathos also provides three convience scripts that are used to establish
secure distributed connections. These scripts are installed to a directory
on the user's $PATH, and thus can be run from anywhere::

    - pathos_tunnel.py              [establish a ssh-tunnel connection]
    - pathos_server.py              [launch a remote RPC server]
    - tunneled_pathos_server.py     [launch a tunneled remote RPC server]

Typing `--help` as an argument to any of the above three scripts will print
out an instructive help message.


License
=======

Pathos is distributed under a modified BSD license.

    >>> import pathos
    >>> print pathos.license()


Citation
========

If you use pathos to do research that leads to publication,
we ask that you acknowledge use of pathos by citing the
following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://dev.danse.us/trac/pathos


More Information
================

Please see http://dev.danse.us/trac/pathos or http://arxiv.org/pdf/1202.1056 for further information.

""" % {'relver' : stable_version, 'thisver' : this_version}

# write readme file
with open('README', 'w') as file:
    file.write(long_description)

# generate 'info' file contents
def write_info_py(filename='pathos/info.py'):
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

# platform-specific instructions
from sys import platform
if platform[:3] == 'win':
    pass
else: #platform = linux or mac
    if platform[:6] == 'darwin':
        pass
    pass

# build the 'setup' call
setup_code = """
setup(name="pathos",
    version='%s',
    maintainer="Mike McKerns",
    maintainer_email="mmckerns@caltech.edu",
    license="BSD",
    platforms=["any"],
    description="a framework for heterogeneous computing",
    long_description = '''%s''',
    classifiers=(
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Physics Programming"),

    packages=['pathos'],
    package_dir={'pathos':'pathos'},
""" % (target_version, long_description)

# add dependencies
pyre_version = '==0.8.2.0-pathos' # NOTE: modified CIG-pyre; includes 'journal'
pp_version = '==1.5.7-pathos'     # NOTE: modified redistribution
dill_version = '>=0.2a.dev'       # NOTE: implicit dependency
pox_version = '>=0.2a.dev'
pyina_version = '>=0.2a.dev'
rpyc_version = '>=3.0.6'
processing_version = '==0.52-pathos' # NOTE: modified redistribution
if has_setuptools:
    setup_code += """
        zip_safe = False,
        dependency_links = ['http://dev.danse.us/packages/'],
        install_requires = ['pp%s','dill%s','pox%s','pyre%s','processing%s'], #'pyina%s'],
""" % (pp_version, dill_version, pox_version, pyre_version, processing_version, pyina_version)

# add the scripts, and close 'setup' call
setup_code += """
    scripts=['scripts/pathos_server.py',
             'scripts/pathos_tunnel.py',
             'scripts/tunneled_pathos_server.py',
             'pathos/portpicker.py'])
"""

# exec the 'setup' code
exec setup_code

# if dependencies are missing, print a warning
try:
    import pyre
    import pp
    if pp.__version__ != pp_version[2:]:
        raise ImportError
    import dill
    import pox
   #import pyina
    try:
        import processing
    except ImportError:
        import multiprocessing
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies is unresolved:"
    print "    pp %s" % pp_version
    print "    pyre %s" % pyre_version
    print "    dill %s" % dill_version
    print "    pox %s" % pox_version
    print "    processing %s" % processing_version
    print "    pyina %s" % pyina_version
    print "***********************************************************\n"

    print """
Pathos relies on modified distributions of '%s', '%s', and '%s'.
Please download and install unresolved dependencies here:
  http://dev.danse.us/packages/
or from the "external" directory included in the pathos source distribution.
""" % ('processing','pp','pyre')


if __name__=='__main__':
    pass

# End of file
