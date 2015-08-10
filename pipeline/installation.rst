
=====================
Pipeline Installation
=====================


This page is currently a copy of the installation guide from the
PBWorks `wiki
<http://hscsurvey.pbworks.com/w/page/64515753/Pipeline%20Installation>`_.

The HSC pipeline is based on the LSST pipeline, so the `instructions
for installing <https://dev.lsstcorp.org/trac/wiki/Installing>`_ that
may prove helpful.  Not everything is the same, however, so try the
below first, and use the LSST instructions as an extra reference if
you run into trouble.  If you can't figure it out, google for the
error, or `e-mail the software group
<mailto:hsc_software@astro.princeton.edu>`_.
 
First, check the `pre-requisites
<https://dev.lsstcorp.org/trac/wiki/Installing/Summer2012>`_ on the
LSST installation instructions.  Ensure the packages listed for your
particular distribution have been installed.  Beyond those, you'll
also need git, a distributed version-control tool.  If you're not
familiar with git, have a look at the `LSST introduction to git
<https://dev.lsstcorp.org/trac/wiki/GitDemoAndTutorial>`_ (you don't
need to understand everything there, just the basics).  Note that an
open port 9148 is required (for the git protocol); if this port is
blocked at your institution, then you'll need to petition for it to be
opened, or use an ssh tunnel.  If you're on a cluster and have
`PBS/Torque <www.adaptivecomputing.com/products/open-source/torque/>`_
for your system (and want to use it), install it now (and see below
about Gotchas for mpich2).  We've also posted a brief outline of
:ref:`how to use the Batch system <back_batch>`.
 
`EUPS <https://github.com/RobertLuptonTheGood/eups>`_ is our product
management tool.  Various guides for it are available including `one
from the LSST wiki <https://dev.lsstcorp.org/trac/wiki/Eups>`_ and one
from :ref:`this site <back_eups>`.  We need to install it before we can do
anything else.  In all of the following, I'll assume you're installing
into /install, and your workspace is in /work; modify these
directories as appropriate.  All our software is designed to be
installed (and used) by an ordinary user, rather than as root, so
don't use sudo or become root.

::

    mkdir -p /install
    cd /work
    git clone git://github.com/RobertLuptonTheGood/eups.git
    cd eups
    ./configure --prefix=/install/eups/default/ --with-eups=/install/
    make install
 
Now, you need to put the following in your ~/.bashrc file::
 
    source /install/eups/default/bin/setups.sh
    export NCORES=$((sysctl -n hw.ncpu || (test -r /proc/cpuinfo && grep processor /proc/cpuinfo | wc -l) || echo 2) 2>/dev/null)
    export MAKEFLAGS="-j $NCORES"
    export SCONSFLAGS="-j $NCORES --setenv"
 
If you use csh or tcsh, then put this in your appropriate shell
startup file (~/.cshrc or ~/.tcshrc)::
 
    source /install/eups/default/bin/setups.csh
 
Now you should run that same command to pick up the EUPS environment
(or source your shell startup file).
 
Now installing the software should be as easy as::

    # bash only
    export EUPS_PKGROOT=http://hsca.ipmu.jp/sumire/packages/
    # (t)csh only
    setenv EUPS_PKGROOT http://hsca.ipmu.jp/sumire/packages/
    eups distrib install hscPipe <version>
 
where <version> is the software version you want (if in doubt, try: eups distrib list hscPipe).
 
Gotchas
-------

mpich
^^^^^

`mpich <www.mpich.org>`_ doesn't seem to be particularly careful in
looking for the headers and libraries for torque.  If these are not
installed in /usr/include and /usr/lib, then you should set the
following environment variables:

* PBS_INCLUDE_DIR: to set the include directory for torque (look for the tm.h header file).
* PBS_LIB_DIR: to set the lib directory for torque (look for the libtorque.so file)
* PBS_DIR: to set both the include and lib directories for torque; this is equivalent to setting PBS_INCLUDE_DIR=$PBS_DIR/include and PBS_LIB_DIR=$PBS_DIR/lib
 
Mac OSX (10.7 and later)
^^^^^^^^^^^^^^^^^^^^^^^^

Mac OSX includes an old gcc front-end to clang that doesn't parse
modern C++ all that well.  To get around this, set::

    export CC=clang
    export CXX=clang++
    SCONSFLAGS+=" cc=clang"

You also need to tell eups that you're going to use the "system"
version of some of the requirements::
 
   cd /work
   git clone git://hsca.ipmu.jp/repos/devenv/buildFiles.git
   eups declare gcc system -r none -m none
   eups declare python system -r none -m none -L buildFiles/python/python.cfg
   eups declare libjpeg system -r none -m none -L buildFiles/libjpeg/libjpeg.cfg
 
Then put the following in your ~/.eups/manifest.remap file, so eups
knows to use these::

    python  system
    gmp     None
    mpfr    None
    mpc     None
    gcc     system
    libjpeg system

    
Ubuntu 12
^^^^^^^^^

On Ubuntu 11.04 (Natty Narwhal) and later (and other systems that have
the linker flags --as-needed activated by default), it is required to
add some additional flags to your environment variables (see also
`LSST's ubuntu-specific setup <https://dev.lsstcorp.org/trac/wiki/Installing/Winter2013#Ubuntu12.04specificstep>`_)::

    export LDFLAGS+=" -Wl,--no-as-needed"
    SCONSFLAGS+=" LINKFLAGS='-Wl,--no-as-needed'"

    
Redhat machines from Mac OSX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On at least some Redhat machines, when installing from a terminal on a
Mac OSX machine (specifically, when TERM=xterm-256color), there is a
python/readline bug that generates escape codes when we attempt to
determine the python version.  There's also a `description of this
problem on stackoverflow
<http://stackoverflow.com/questions/15760712/python-readline-module-prints-escape-character-during-import>`_).
The workaround is to do::

    export TERM=vt100
 
 
SSL certificate errors
^^^^^^^^^^^^^^^^^^^^^^

If you see SSL certificate errors in the build log, try doing this and
then eups distrib install::

    curl () { /usr/bin/curl -k "$@"; } export -f curl

    
Intel Math Kernel Library (MKL)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

mosaic.py can take a long time unless you've compiled it with mkl
(note that mkl is neither "free" as in beer or "free" as in speech).
Setting up mkl may be problematic, because it seems installations vary
from machine to machine, or version to version.  You may have to do
some hacking or playing around.  E-mail the software team if you get
stuck.

To set up mkl, grab the buildFiles product::

    git clone git://hsca.ipmu.jp/repos/buildFiles.git
    cd buildFiles
    
Edit the line that sets MKL_SYSTEM_DIR so that it uses the correct
directory for your installation of mkl.  (You may also have to play
around with the other lines so that the LD_LIBRARY_PATH gets set
correctly.)  Then you can::

    eups declare mkl VERSION -M mkl.table -r none -L mkl/mkl.cfg
    
You should then put the following in your ~/.eups/manifest.remap::

    mkl    VERSION

(Replace the two instances of VERSION above with the appropriate version name.)

Note that this doesn't rebuild meas_mosaic to use mkl, just makes mkl
available for the next time it's build through eups distrib install.
To rebuild meas_mosaic, do::

    git clone git://hsca.ipmu.jp/repos/meas_mosaic.git
    cd meas_mosaic
    setup hscPipe <LATEST_VERSION> # replace with the appropriate version
    setup -j -r .
    setup -j mkl VERSION
    scons opt=3
    
Alternatively, you may, after noting the appropriate version of meas_mosaic::

    setup meas_mosaic <LATEST_VERSION>
    setup -j mkl VERSION
    eups distrib install -jF meas_mosaic <LATEST_VERSION>
    
If you get an error message "This Intel <math.h> is for use with only the Intel compilers" (or similar), try hacking the CPPFLAGS setting in mkl.cfg (e.g., remove the entry).


.. _astrometry_net_data:

AstronometryNetData catalog
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The astrometry_net_data product distributed with the pipeline is a
placeholder, and not a real astrometry catalogue. You need to obtain,
declare and setup a proper astrometry_net_data.

**Obtaining**:

If you have an account on another machine that has some
astrometry_net_data catalogues (e.g., the IPMU clusters), you can copy
over the directories listed when you do::

    eups list -d astrometry_net_data
    
If you can't do that, you can get the 2mass catalogue from
`astrometry.net <http://broiler.astrometry.net/~dstn/4200/HSC/>`_. It
will need an additional file called andConfig.py that looks like
this::


    root.defaultMagColumn = "j_mag"      # Default column name to use for magnitudes
    root.magColumnMap = { 'J': 'j_mag' } # Mapping from filter to magnitude column name
    root.magErrorColumnMap = {}          # Mapping from filter to magnitude error column name
    root.indexFiles = ['index-130202000-00.fits',
                       'index-130202000-01.fits',
                       # Etc, listing all the index files
                      ]

                      
There is also an SDSS DR8 catalog that you can download from `here
<http://hsca.ipmu.jp/sumire/astrometry_net_data/sdss-dr8/>`_.

**Declaring**:

For each astrometry_net_data directory you've downloaded, you need to::

    eups declare astrometry_net_data <version> -r /path/to/astrometry_net_data/<version> -m none
    
When I have multiple directories, the following is helpful::

    cd /path/to/astrometry_net_data
    for d in *; do eups declare astrometry_net_data $d -r $d -m none; done
    
**Setup**:

Once the catalogue you want has been declared to eups, you should set
it up so you can use it::

    setup -j astrometry_net_data <version>
  
    # e.g.;
    setup -j astrometry_net_data sdss-dr8
    
The ``-j`` flag means only ``setup`` this product: it doesn't mess
with any dependencies. This is important because without it, it will
try to ``unsetup`` the dependencies (e.g., ``gcc`` and ``python``),
and leave you in a bad state.

You will need to ``setup`` the ``astrometry_net_data`` in each new
environment, e.g., whenever you ``setup -t HSC hscPipe``.

