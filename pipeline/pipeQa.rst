

======
PipeQA
======

.. contents::
   :local:
   :depth: 2


Introduction
------------

Once you've run the single-frame or coadd-processing, the pipeline
includes a system for quality assurance of the outputs.  The system
consists of two packages ``testing_displayQA`` (a web-based display
tool), and ``testing_pipeQA`` (a pipeline-based tool for generating
figures and testing values).  The system requires a web server and a
database, with different options available for each (see Dependencies
below).

Dependencies
------------

If you have a large dataset, an Apache+PostgreSQL installation is a
faster and more flexible option.  However, if you're running only a
small amount of data, or your system isn't running Apache or
PostgreSQL and you don't wish to install them, The PHP and/or Sqlite
options may be a better choice.

Apache + PostgreSQL option (More difficult to install, but runs faster)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is really the standard way of installing PipeQA.  The PostgreSQL
database is able to handle multiple connections, allowing PipeQA to
run parallelized.  This is preferred, if you can do it, but not
necessary.  And, although the steps are briefly listed here, the
actual installation and setup can be difficult, and isn't described
here.

* Install/start apache

    * install php, php-pdo, and php-pgsql (e.g. with yum on a redhat system)::

        $ yum install php
        $ yum install php-pdo
        $ yum install php-pgsql

* Install/start postgresql

    * createdb ...
    * create user ... (set privileges for create table)


PHP + Sqlite option (Easier to install [user-level], but slower to run)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't have root permission on your system, or you just don't
wish to install/run Apache and PostgreSQL; Sqlite (included with the
pipeline) is a suitable database, and a recent versions of PHP (> 5.4)
can be used to provide a light-weight web server.

Current versions of PHP can be found at `PHP
<http://php.net/downloads.php>`_.  Most Linux systems use PHP version
5.3 by default, and it does not include the web server.

* Install PHP version > 5.4.  This will install into your $HOME/usr
  directory (make that directory if it doesn't exist), and won't
  interfere with the system installation.  The build follows the
  standard GNU make style::

   $ tar xvzf php-tarball.tar.gz
   $ cd php/
   $ ./configure --prefix=$HOME/usr
   $ make
   $ make install

* A light-weight webserver can now be run as a user with (visible from
  localhost:8000/)::

   # cd to directory you wish to serve
   $ cd $HOME/directory/to/serve/

   # start the server on a port larger than 1024 (8000 shown here)
   $ ~/usr/bin/php -S localhost:8000 -t .


Quick Start
-----------

First, go and install/setup either (1) Apache+PHP+PostgreSQL, or (2)
PHP > 5.4 (see above).  Each step shown here is described in greater detail below.

Apache with PostgreSQL
^^^^^^^^^^^^^^^^^^^^^^

::

    # confirm your database connection settings
    $ cat ~/.pqa/db-auth.py
    host = "postgresdb.master.ipmu.jp"
    port = "5432"
    user = "username"
    password = "secret"
    dbsys = "pgsql"

    # set environment and create a place for QA reruns
    $ export WWW_ROOT=$HOME/public_html/qa
    $ mkdir $WWW_ROOT
    $ export WWW_RERUN=cosmos
    $ export PGPASSWORD=secret

    # create the site, and run QA
    $ newQa.py -c green -p hsc $WWW_RERUN
    $ hscPipeQa.py /data/Subaru/HSC --rerun cosmos --id visit=1000..1020:2 ccd=0..103 -j 20

    # Go see your site at http://master.ipmu.jp/~username/qa/cosmos/

PHP with Sqlite
^^^^^^^^^^^^^^^

::

    # confirm your settings
    $ cat ~/.pqa/db-auth.py
    dbsys = "sqlite"

    # set environment and create a place for QA reruns
    $ export WWW_ROOT=$HOME/public_html/qa
    $ mkdir $WWW_ROOT
    $ export WWW_RERUN=cosmos

    # create the site, and run QA
    $ newQa.py -c green -p hsc $WWW_RERUN
    $ hscPipeQa.py /data/Subaru/HSC --rerun cosmos --id visit=1000^1002 ccd=0..103 -j 2

    # Start a local PHP web server
    $ cd ~/public_html/
    $ php -S localhost:8000 -t .
    
    # Go see your site at http://localhost:8000/qa/cosmos/


Configuration
-------------

The connection information for the database is needed to run pipeQA and this is stored in a parameter file which lives in your directory ``~/.pqa/db-auth.py``.  Here's an example used on master.ipmu.jp::

    $ cat ~/.pqa/db-auth.py
    host = "postgresdb.master.ipmu.jp"
    port = "5432"
    user = "username"
    password = "secret"
    dbsys = "pgsql"

For Sqlite, the host, port, user, and password aren't needed, and the file need only specify ``dbsys = 'sqlite'``::

    $ cat ~/.pqa/db-auth.py
    dbsys = "sqlite*


.. ::
    * ~/.hsc/db-auth.paf (db where pipeQA loads data from [currently not enabled])::

    database: {
        authInfo: {
            host: "157.82.237.169"
            port: "5432"
            user: "kensaku"
            password: "secret"
        }
    }

PipeQA uses two environment variables: ``WWW_ROOT``, and
``WWW_RERUN``.  If using PostgreSQL, a third variable ``PGPASSWORD``
is convenient and saves typing your password (note that this keeps
your database password in clear text in an environment variable!)::

    # where PipeQA will create QA rerun directories
    $ export WWW_ROOT=$HOME/public_html/qa

    # where PipeQA will store files for a given rerun in $WWW_ROOT/$WWW_RERUN
    # If using PostgreSQL, the database created by newQa.py will be called pqa_<WWW_RERUN>
    $ export WWW_RERUN=cosmos

    # (PostgreSQL only) If not set, you'll be prompted for it when running newQa.py
    $ export PGPASSWORD=secret
    

Creating a QA Site with newQa.py
--------------------------------

Before you can run QA on a dataset, you must create the display site online with ``newQa.py``::

    $ newQa.py -c green -p hsc $WWW_RERUN

This will create a new QA rerun in the WWW_ROOT directory.  It will
use a green CSS style with HSC logos.  If using PostgreSQL, a new
database pqa_<WWW_RERUN> will also be created.  Options available
include::

    -c {blue,green,red,brown}, --color {blue,green,red,brown}
                          Specify style color.
    -f, --force           Force a reinstall if already exists.
    -F, --forceClean      Force a reinstall and remove existing data
    -r ROOT, --root ROOT  Override WWW_ROOT.
    -n, --noquery         Don't query about options ... user knows what user is
                          doing.
    -p {lsst,hsc,sc}, --project_icons {lsst,hsc,sc}
                          Specify project-specific icons (favicon which appears on browser tab).



Running PipeQA
--------------

PipeQA is able to run in a variety of ways.  The main usage is to
processing outputs from a rerun and perform a series of tests and
sanity checks on your results.  When run in this way, the results are
compared to catalog values.  However, there are times when you may
want to compare two data sets to one another (e.g. two visits of the
same field) or two reruns of the same data (e.g. the same data
processed with different parameters).  These two methods of running
are discussed separately:

Regular PipeQA
^^^^^^^^^^^^^^

This section describes PipeQA as it is normally used - to assess the
quality of pipeline outputs in a specific rerun.


**Using Python's Multiprocessing**

**Avoid using many cores with Sqlite!** The Sqlite database cannot
  handle concurrency (multiple threads) very well (it uses
  file-locking), and your QA run may become very slow if you try to
  use more than a few threads.  This should not be a problem for a
  PostgreSQL database until more than ~20 threads are used.

* single-frame (-j 20 uses 20 CPU cores on the current node)::

    $ hscPipeQa.py /data/Subaru/HSC --rerun my_rerun --id visit=1234..1240:2 ccd=0..103 -j 20

* coadd QA (-j 2 uses 2 CPU cores on the current node)::

    $ hscCoaddQa.py /data/Subaru/HSC --rerun my_rerun --id tract=0 patch=5,4^5,5 filter=HSC-I -j 2

    
**Using Batch Processing**


* single-frame, 4 nodes with 8 processes per node.  (NOTE: --mpiexec='-bind-to socket', but will improve performance)::

    $ poolPipeQa.py /data/Subaru/HSC --rerun my_rerun --id visit=1234..1240:2 ccd=0..103 --job=poolqa --nodes=4 --procs=8 --mpiexec='-bind-to socket'

* Coadd, 4 nodes with 8 processes per node.  (NOTE: --mpiexec='-bind-to socket', but will improve performance)::

    $ poolCoaddQa.py /data/Subaru/HSC --rerun my_rerun --id tract=0 filter=HSC-I --job=poolcoadd --nodes=4 --procs=8 --mpiexec='-bind-to socket'


Comparison PipeQA
^^^^^^^^^^^^^^^^^

This section describes PipeQA when it is run to compare directly
between two different reruns, or between different datasets in the
same rerun.  The comparison tasks can only be run with Python's
multiprocessing, and can not yet be run through the batch processing
system.

**Visit to Visit**

To compare two visits in the same rerun (assuming the CCDs you select overlap)::

    $ hscPipeCompare.py /data/Subaru/HSC --rerun=cosmos --id visit=1236 ccd=0..103 --refVisit=1238

**Rerun to Rerun (single-frame)**

To compare results on a dataset processed twice with two reruns (e.g. to determine the effect of changing pipeline parameters)::

    $ hscPipeCompare.py /data/Subaru/HSC --rerun=cosmos --id visit=1236 ccd=0..103 --refRerun=cosmos2

**Rerun to Rerun (coadd)**

When comparing coadds, only rerun-to-rerun comparison is possible as tracts and patches cover separate regions (unlike visits, which may cover the same pointing exactly)::

    $ hscCoaddCompare.py /data/Subaru/HSC --rerun=cosmos --id tract=0 patch=5,5 filter=HSC-I --refRerun=cosmos2


**Coadd to Visit**

One other comparison that may be of interest is a comparison between coadd data and a single-frame visit.  that can be accomplished with::

    $ hscCoaddCompare.py /data/Subaru/SSP --rerun=cosmos --id tract=0 patch=5,5 filter=HSC-I --refVisit=1236



Removing a Visit or Tract from a Rerun with delQa.py
----------------------------------------------------

Basic Usage::

    $ delQa.py $WWW_RERUN <group> -p [-n]

    # -n is no-op
    # -p is a verbose (print)

    
The ``<group>`` referred-to is the text string which defines the visit
or tract.  For single frame data, it would look like e.g. '1234-i' for
visit number 1234 in i-band.  For a coadd, it would have the form
'9375-HSC-I-i' for a tract number 9375 observed in HSC-I (the repeated
'i' is also the filter ... apologies for a possibly-confusing
implementation detail).

If you want to see which files will be deleted and which lines will be
dropped from the database, run with the ``-n`` option.  This will
report the plan, but will not actually remove anything.

``-p`` will make the output a bit more verbose.:


E.g. to remove a given tract from a Coadd QA run.  See the online QA site for the text key
name of the testset.  In this case, tract 9375 in HSC-I band is being
removed from a rerun called ``mergetest``::
    
    $ delQa.py mergetest 9375-HSC-I-i -p


