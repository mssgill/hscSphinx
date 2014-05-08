

======================
Background Information
======================

There are a variety of things which are common to all tasks associated
with a processing run.  Some of the things are just basic terminology
that you'll need to communicate with developers, while others are of
more practical importance for actually running the pipeline code
effectively.



.. _prep_eups:

EUPS
----

EUPS is the in-house package manager used by LSST and HSC.  It was
originally developed by Nikhil Padmanabhan during the SDSS survey, and
has since been rewritten (and then re-rewritten) to manage the LSST
and HSC code.  The term package manager here refers to a system like
`yum` (Redhat Linux), `apt-get` (Debian Linux), Macports (OSX), or
Homebrew (OSX).  When you wish to install some software package, the
required dependencies can be a complicated mess to sort out, and
package managers are meant to handle this for you.  The EUPS is used
here because it has some additional functionality that the others
lack.  Namely, it permits a user to use different versions of the same
software.  Rather than installing e.g. FFTW and then having to use
that installed version, EUPS lets you install several versions, and
choose which one you'd like to work with at a given time.  Different
users (or the same user) can all use different versions
simultaneously.

In order to enable EUPS in your current shell, you must source a
script appropriate for the shell you're using.  Note that you must
source the file, not execute it::

    # in a bash shell
    $ source /data1a/ana/products2014/eups/default/bin/setups.sh

    # in a csh shell (or tcsh)
    $ source /data1a/ana/products2014/eups/default/bin/setups.csh

Doing this sets a number of shell functions and environment variables
that enable eups commands in your current shell.  Since you'll have to
do this in every shell where you intend to work, you probably want to
create an alias for it in your `~/.bashrc` (or `~/.cshrc`), or simply
source the setups.sh file directly there::

     # from .bashrc
     alias setupHsc='source /data1a/ana/products2014/eups/default/bin/setups.sh'

Then you can enable EUPS with::

     $ setupHsc

     
Here are the most common eups commands.

#. `help`::
    
     $ eups -h


#. `list` ... show the packages which are installed on the system::

     # see everything
     $ eups list

     # see all installed versions of obs_subaru
     $ eups list obs_subaru
     
     # see all packages called obs_*
     $ eups list obs_*
     
     # see what's currently 'setup'
     $ eups list -s

     
#. `setup` ... enable a specific software version with all it's dependencies::

     # setup the HSC pipeline, version 2.12.0f_hsc  (-v is 'verbose')
     $ setup -v hscPipe 2.12.0f_hsc
     
     # setup the HSC pipeline using the versions tagged 'HSC' (the developer recommended version)
     $ setup -v hscPipe -t HSC
    

     
    
Setting up for a run
^^^^^^^^^^^^^^^^^^^^

In general, in order to do most things with the HSC pipeline, you'll
want to do the following: (1) enable EUPS, (2) setup the pipeline,
and (3) setup a calibration catalog (described more in the pipeline
section)::

    $ setupHsc
    $ setup -v hscPipe -t HSC
     
* For the calibration catalog, CHOOSE ONLY ONE!  A `setup` command will override it's predecessor!::
    
    # perhaps use PS1
    $ setup -v astrometry_net_data ps1_pv1.2a
    
    # *OR* perhaps use SDSS DR8
    $ setup -v astrometry_net_data sdss-dr8

    

.. _prep_torque:


PBS/TORQUE
----------

Our batch processing is handled with a system called TORQUE, which is
a popular variant of PBS (Portable Batch System).  The system handles
job scheduling and queue management for parallel jobs being run on
distributed compute nodes.  For the purposes of running the HSC
pipeline, there are only a handful of commands you'll need to concern
yourself with, mainly checking the status of your job, and possibly
cancelling it.  An example of each is shown below.

On your first attempt to connect to a cluster node, you won't have the
compute node listed in your .ssh/known_hosts, and the connection
attempt will query you (you've seen this when making any ssh
connection for the first time).  However, this user-query will cause a
submitted job to fail as the batch system can't answer 'yes' on your
behalf.  The easiest way to deal with this is to override the host
checking for the hosts on the cluster.  On this example cluster, the
compute nodes are all called analysisXX, so adding the following lines
to your ~/.ssh/config will disable host checking only for cluster
nodes::

    $ cat ~/.ssh/config
    Host an*
        StrictHostKeyChecking no


There may be various 'queues' defined on a Torque system, with each
having different levels of access to resources (i.e. the max number of
nodes you can request that your job gets to run on).  The `qstat -Q`
command will show you the currently defined queues on the system, and
`qstat -Q -f` will show full information.  In general, we've set
queues with large node limits to allow fewer jobs to run, while those
with small node limits will allow many jobs to run.  When you submit a
job, please submit to the smallest queue you think you can afford to
use.

        
qstat
^^^^^
        
Use 'qstat' to check the status of a job.  The '-a' option provides a
bit more info.  Much more info is available in 'man qstat', but this
simple example should give the basic idea.  The example shows a single
job in the queue.  It's run by the user 'you' and is running in the
quene named 'small'.  It uses 3 nodes, and is currently running 'R'::

    $ qstat -a
    master: 
    .                                                                Req'd    Req'd       Elap
    Job ID        Username    Queue    Jobname   SessID  NDS   TSK   Memory   Time    S   Time
    ------------- ----------- -------- --------- ------ ----- ------ ------ --------- - ---------
    374.master    you         small    myjob        --      3     36    --   01:06:40 R  00:00:02


For reference, here are the job status codes::
  
    C -  Job is completed after having run/
    E -  Job is exiting after having run.
    H -  Job is held.
    Q -  job is queued, eligible to run or routed.
    R -  job is running.
    T -  job is being moved to new location.
    W -  job is waiting for its execution time
         (-a option) to be reached.
    S -  (Unicos only) job is suspend.


Here are the most popular options used with `qstat`::

    $ qstat -q          list all queues
    $ qstat -Q          list all queues with more info
    $ qstat -Q -f       list all queues with full information
    $ qstat -a          list all jobs
    $ qstat -au userid  list jobs for userid
    $ qstat -r          list running jobs
    $ qstat -f job_id   list full information about job_id
    $ qstat -Qf queue   list full information about queue
    $ qstat -B          list summary status of the job server
    
    
qdel
^^^^

Occassionally, something goes wrong with a job.  Perhaps you submit
with the wrong command line arguments, or the job is just taking too
long to finish; whatever the reason, `qdel` can be used to kill the
job.  Use qstat to determine the job ID, and then kill it as follows
(assuming the job ID from the above example)::

    $ qdel 374

More info is available with `man qdel`.


Pipeline TORQUE-related arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The pipeline tasks which use TORQUE (e.g. ``reduceFrames.py``, and
``stack.py``) allow you to specific how your job will make use of the
system resources; specifically, which queue, how many nodes, how many
cores per node.  When you start running any of the
``reduce<thing>.py`` commands (``reduceBias.py``, ``reduceFlat.py``,
``reduceFrames.py``, etc., you'll be able to use the following
arguments to control TORQUE's behaviour:


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



Reruns
------

The term ``rerun`` originated in SDSS.  It simply refers to a single
processing run, performed with a specified version of the reduction
code, and with a specific set of configuration parameters.  The
assumption is that within a given 'rerun', the data have been handled
in a homogeneous way.

.. todo::

    This is repeated in the glossary.  Are both places needed?  It's
    short, and won't change.

    
.. _general_dataId:

The dataId
----------

A 'dataId' is a unique identifier for a specific data input.  The two
forms you most likely need to familiarize yourself with are the
'visit','ccd' identifiers used to refer to a specific CCD in a
specific exposure (called a 'visit'); and 'tract','patch' identifiers
which refer to the coordinate system used in coadded images.  Other
important keys in a dataId might include:

* field (name you gave your target in the FITS header 'OBJECT' entry)
* dateObs (the date of observation from the FITS header 'DATE-OBS' entry)
* filter  (again from the FITS header ... 'FILTER' entry)

In almost any pipeline command you can specify which data you wish to
process with ``--id <dataID>``, e.g.::

    # run visit 1000, CCD 50
    $ hscProcessCcd.py /data/ --id visit=1000 ccd=50

    # run all the HSC-I data from M87 taken on Jan 15, 2015
    $ hscProcessCcd.py /data/ --id field=M87 filter=HSC-I dateObs=2015-01-15

    # run tract 0 patch 1,1  in HSC-I for a coadd (here you'll need the filter too)
    $ hscProcessCoadd.py /data/ --id tract=0 patch=1,1 filter=HSC-I

Only a few of the dataId components are ever needed to uniquely
specify a given data input or output.  For example, the observatory
will never reuse the number assigned as a 'visit', so it's impossible
to have the same visit with a different filter or dateObs.  Once you
specify the visit, the other values are almost all redundant.  This isn't
true for tracts and patches, though!  A tract,patch refers to a
location on the sky and can have multiple filters or dateObs values.


Configuration Parameters
------------------------

A variety of things about the pipeline are configurable through either
command-line arguements, or as settings in configuration parameter
files.  At last count, there were approximately 1 bazillion
configuration parameters.  The overwhelming majority of them are
things that you'll never even need to be aware of, much less modify.

Configuration parameters have a hierarchical form, with each parameter
belonging to a specific pipeline module called a 'Task', and each
nested sub-task separated by a decimal point.  For example, the
'instrument signature removal' task (ISR, responsible for bias
subtraction, flat fielding, etc.) has a configurable parameter
``doFringe``::

    isr.doFringe=True

All of configuration parameters have a default value which should be
what most users want, but if you need to override some you have two
options: command line arguments, or a configuration file (or a bit of
both).

* To override a parameter on the command line, use ``--config
  name=value`` (or just ``-c name=value``)::

    --config isr.doFringe=False

* To override a parameter in a configuration file, put the parameters
  in a text file, one per line, and use ``--configfile filename`` (or
  just ``-C filename``) to load the parameters.

