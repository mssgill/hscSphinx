

======
PipeQA
======

.. contents::
   :local:
   :depth: 2



Quick Start
-----------

::

    $ cat ~/.pqa/db-auth.py
    host = "postgresdb.master.ipmu.jp"
    port = "5432"
    user = "username"
    password = "secret"
    dbsys = "pgsql"

    $ export WWW_ROOT=$HOME/public_html/qa
    $ mkdir $WWW_ROOT
    $ export WWW_RERUN=cosmos
    $ export PGPASSWORD=secret
    
    $ newQa.py -c green -p hsc $WWW_RERUN
    $ hscPipeQa.py /data/Subaru/HSC --rerun cosmos --id visit=1000..1020:2 ccd=0..103 -j 20
    
    

Dependencies
------------

* start apache

    * install php, php-pdo, and php-pgsql::

        $ yum install php
        $ yum install php-pdo
        $ yum install php-pgsql
        
* start postgresql

    * createdb
    * create user (set privs for create table)
    

Configuration
-------------

* ~/.pqa/db-auth.py  (db where pipeQA will store it's results)::

    host = "postgresdb.master.ipmu.jp"
    port = "5432"
    user = "username"
    password = "secret"
    dbsys = "pgsql"


* ~/.hsc/db-auth.paf (db where pipeQA loads data from [currently not enabled])::

    database: {
        authInfo: {
            host: "157.82.237.169"
            port: "5432"
            user: "kensaku"
            password: "secret"
        }
    }

* export the ``WWW_ROOT``, ``WWW_RERUN``, and ``PGPASSWORD`` environment variables::

    # where PipeQA will create QA rerun directories
    $ export WWW_ROOT=$HOME/public_html/qa

    # where PipeQA will store files for a given rerun in $WWW_ROOT/$WWW_RERUN
    # It will also attempt to connect to a PostgreSQL database called pqa_<WWW_RERUN>
    #   (created with newQa.py)
    $ export WWW_RERUN=cosmos

    # If you don't set this, you'll be prompted for it when running newQa.py
    $ export PGPASSWORD=secret
    

Creating a QA Site with newQa.py
--------------------------------

* Before you can run QA on a dataset, you must create the display site online with newQa.py::

    $ newQa.py <WWW_RERUN>

This will create a new QA rerun in the WWW_ROOT directory.  A new
database pqa_<WWW_RERUN> will also be created in PostgreSQL.  Some options available include::

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

Using Python's Multiprocessing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* single-frame (-j 20 uses 20 CPU cores on the current node)::

    $ hscPipeQa.py /data/Subaru/HSC --rerun my_rerun --id visit=1234..1240:2 ccd=0..103 -j 20

* coadd QA (-j 2 uses 2 CPU cores on the current node)::

    $ hscCoaddQa.py /data/Subaru/HSC --rerun my_rerun --id tract=0 patch=5,4^5,5 filter=HSC-I -j 2

    
Using PBS/Torque Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
* single-frame, 4 nodes with 8 processes per node.  (NOTE: --mpiexec='-bind-to socket', but will improve performance)::

    $ poolPipeQa.py /data/Subaru/HSC --rerun my_rerun --id visit=1234..1240:2 ccd=0..103 --job=poolqa --nodes=4 --procs=8 --mpiexec='-bind-to socket'

* Coadd, 4 nodes with 8 processes per node.  (NOTE: --mpiexec='-bind-to socket', but will improve performance)::

    $ poolCoaddQa.py /data/Subaru/HSC --rerun my_rerun --id tract=0 filter=HSC-I --job=poolcoadd --nodes=4 --procs=8 --mpiexec='-bind-to socket'




Removing a Visit or Tract from a Rerun with delQa.py
----------------------------------------------------

Basic Usage::

    $ delQa.py $WWW_RERUN <group> -p [-n]

    # -n is no-op
    # -p is a verbose (print)

    
The ``<group>`` referred-to is the text string
which defines the visit or tract.  For single frame data, it would
look like e.g. '1234-i' for visit number 1234 in i-band.  For a coadd,
it would have the form '9375-HSC-I-i' for a tract number 9375 observed
in HSC-I (the repeated 'i' is also the filter ... apologies for a
possibly-confusing implementation detail).

If you want to see which
files will be deleted and which lines will be dropped from the
database, run with the ``-n`` option.  This will report the plan, but
will not actually remove anything.

``-p`` will make the output a bit
more verbose.::


E.g. to remove a given tract from a Coadd QA run.  See the online QA site for the text key
name of the testset.  In this case, tract 9375 in HSC-I band is being
removed from a rerun called ``mergetest``::
    
    $ delQa.py mergetest 9375-HSC-I-i -p


Writing a New QA Test
---------------------

Just copy an existing one.


