
=====================
General Pipeline Info
=====================

There are a variety of things which are common to all tasks associated
with a processing run.  Some of the things are just basic terminology
that you'll need to communicate with developers, while others are of
more practical importance for actually running the pipeline code
effectively.


Reruns
------

The term ``rerun`` dates back to SDSS.  It simply refers to a single
processing run of a set of data performed with a specified version of
the reduction code, and a specific set of configuration parameters.
The assumption is that within a given 'rerun', the data have been
handled in a homogeneous way.


The dataId
----------

A 'dataId' is a unique identifier for a specific data input.  The two
forms you most likely need to familiarize yourself with are the
'visit','ccd' identifiers used to refer to a specific CCD in a
specific exposure (called a 'visit'); and 'tract','patch' identifiers
which refer to the coordinate system used in coadded images.  Other important keys in a dataId might include:

* field (name you gave your target in the FITS header 'OBJECT' entry)
* dateObs (the date of observation from the FITS header 'DATE-OBS' entry)
* filter  (again from the FITS header ... 'FILTER' entry)

In almost any pipeline command you can specify which data you wish to process with ``--id dataID``, e.g.::

    # run visit 1000, CCD 50
    $ hscProcessCcd.py /data/ --id visit=1000 ccd=50

    # run all the HSC-I data from M87 taken on Jan 15, 2015
    $ hscProcessCcd.py /data/ --id field=M87 filter=HSC-I dateObs=2015-01-15

    # run tract 0 patch 1,1  in HSC-I for a coadd (here you'll need the filter too)
    $ hscProcessCoadd.py /data/ --id tract=0 patch=1,1 filter=HSC-I

Only a few of the dataId components are ever needed to uniquely
specify a given data input or output.  The observatory will never
reuse the number assigned as a 'visit', so it's impossible to have the
same visit with a different filter or dateObs.  Once you specify the
visit, the values are almost all redundant.  This isn't true for
tracts and patches, though!  A tract,patch refers to a location on the
sky and can have multiple filters or dateObs values.
    

.. _torque_args:

Torque-related batch processing arguments
-----------------------------------------

Some of the pipeline tasks (e.g. ``reduceFrames.py``, and
``stack.py``) use PBS TORQUE to manage batch processing.  If you
haven't yet familiarized yourself with TORQUE, please take a look at
our brief :ref:`TORQUE Summary <prep_torque>`, as it will help to
understand what these command line arguements actually do.

The arguments you need to concern yourself with are:

``--job``

    This is the name of the job, as you want it to appear in ``qstat``
    commands.  It will also be used in the name of the log files that
    TORQUE writes containing the ``stdout`` from your job.

``--queue``

    The name of the queue you're submitting your job to.  There may be
    multiple queues on the system you're using.  You can see which
    ones there are with::

    $ qmgr -c 'print server'

``--nodes``

    Specify the number of nodes you want your process to use.  Note
    that if you ask for too many, you'll get an error message telling
    you so.  The maximum number of nodes you're allowed to request
    from a given queue is listed in the output of ``qmgr -c 'print
    server'`` with label ``resources_max.nodes``.

``--procs``

    Specify the number of processes on each node you want your process
    to use.  Again, you'll have to be careful not to exceed the
    specifications for the queue you've requested.  Check ``qmgr -c
    'print server'`` to find ``resources_max.ncpus``, and make sure
    that ``procs`` times ``nodes`` (i.e. the total number or CPUs
    you're asking for) isn't larger than ``resources_max.ncpus``.

``--time``

    Use this to adjust the expected execution time for each element.
    TORQUE may time-out your job if it takes longer than expected, so
    this allows you to increase the limit.

    
``--do-exec``

    This will cause the system to run the code in the current shell,
    rather than submitting to TORQUE system.  It can be very useful
    for debugging specific problems, but shouldn't ever be used for a
    large job (it would just take too long!).
    
``--pbs-output``

.. todo::    I haven't played with this.  Paul? What does it do?


Configuration Parameters
------------------------


