

====================================
General Info about Pipeline commands
====================================

The pipeline is a collection of commands which each perform a very
specific function: combine biases or flats, process single exposures,
build and process coadds, etc.  These are commands are built with a
common set of tools and there are a handful of command line options
which are available with almost all of the commands.  This section
includes a bit of information about these options.  The examples will
use the single-frame processing command ``hscProcessCcd.py``, but
these things should be available with all pipeline commands.


Help
----

You can always request ``--help``, or just ``-h``.  Here's what it
looks like, with each item explained in greater detail below::

    $ hscProcessCcd.py -h
    usage: hscProcessCcd.py input [options]

    positional arguments:
      ROOT                  path to input data repository, relative to
                            $PIPE_INPUT_ROOT

    optional arguments:
      -h, --help            show this help message and exit
      --calib RAWCALIB      path to input calibration repository, relative to
                            $PIPE_CALIB_ROOT
      --output RAWOUTPUT    path to output data repository (need not exist),
                            relative to $PIPE_OUTPUT_ROOT
      --rerun [INPUT:]OUTPUT
                            rerun name: sets OUTPUT to ROOT/rerun/OUTPUT;
                            optionally sets ROOT to ROOT/rerun/INPUT
      -c [NAME=VALUE [NAME=VALUE ...]], --config [NAME=VALUE [NAME=VALUE ...]]
                            config override(s), e.g. -c foo=newfoo bar.baz=3
      -C [CONFIGFILE [CONFIGFILE ...]], --configfile [CONFIGFILE [CONFIGFILE ...]]
                            config override file(s)
      -L LOGLEVEL, --loglevel LOGLEVEL
                            logging level
      -T [COMPONENT=LEVEL [COMPONENT=LEVEL ...]], --trace [COMPONENT=LEVEL [COMPONENT=LEVEL ...]]
                            trace level for component
      --debug               enable debugging output?
      --doraise             raise an exception on error (else log a message and
                            continue)?
      --logdest LOGDEST     logging destination
      --show [{config,data,tasks,run} [{config,data,tasks,run} ...]]
                            display the specified information to stdout and quit
                            (unless run is specified).
      -j PROCESSES, --processes PROCESSES
                            Number of processes to use
      -t PROCESSTIMEOUT, --process-timeout PROCESSTIMEOUT
                            Timeout for multiprocessing; maximum wall time (sec)
      --clobber-output      remove and re-create the output directory if it
                            already exists (safe with -j, but not all other forms
                            of parallel execution)
      --clobber-config      backup and then overwrite existing config files
                            instead of checking them (safe with -j, but not all
                            other forms of parallel execution)
      --id [KEY=VALUE1[^VALUE2[^VALUE3...] [KEY=VALUE1[^VALUE2[^VALUE3...] ...]]
                            data ID, e.g. --id visit=12345 ccd=1,2


.. glossary::                           
                            
    ROOT
        This is the path to your input :ref:`data repository <data_repo>`.

    -h, --help
        Show this help message and exit.  This may vary slightly for different commands.
    
    --calib RAWCALIB    
        Path to input calibration repository.  In general, you don't
        need to specify this.  If you follow the instructions for
        :ref:`making detrends <detrend>`, the calibration products
        will be installed in your data repo in the correct place.
                            
    --output RAWOUTPUT
        Path to output data repository (need not exist).  You may
        encounter situations where you want to load data from one
        rerun, but write processed outputs in a different place.  This
        ``--output`` option will let you do that.  For an example, see
        :ref:`writing coadds to a different output rerun <coadd_rerun_change>`.
        
    --rerun [INPUT:]OUTPUT
    
        Rerun name: sets OUTPUT to ROOT/rerun/OUTPUT; optionally sets
        ROOT to ROOT/rerun/INPUT.  You almost always just want to set
        this to a single value.  Any inputs will be loaded from that
        rerun, and any outputs will be written there.  Adding
        ``:OUTPUT`` will cause your outputs written to a different
        rerun within the same data repo.  For an example, see
        :ref:`writing coadds to a different output rerun
        <coadd_rerun_change>`.
        
    -c [NAME=VALUE [NAME=VALUE ...]], --config [NAME=VALUE [NAME=VALUE ...]]    
        Override specific config parameters, e.g. ``-c foo=newfoo
        bar.baz=3``.  If you have many such parameters, you probably
        want to put them in a file and use ``-C`` to load them.
        
    -C [CONFIGFILE [CONFIGFILE ...]], --configfile [CONFIGFILE [CONFIGFILE ...]]
        Provide override config parameters in a file ... one per line.
        For a bit more info, see :ref:`here <back_config>`.
        
    -L LOGLEVEL, --loglevel LOGLEVEL    
        Specify the level of logging messages.  Choices are ``DEBUG``
        (ridiculous numbers of messages), ``INFO`` (basic information
        [default]), ``WARN`` (only warnings), ``FATAL`` (only complete
        pipeline failures).
        
    -T [COMPONENT=LEVEL [COMPONENT=LEVEL ...]], --trace [COMPONENT=LEVEL [COMPONENT=LEVEL ...]]
    
        'Trace' logging isn't as widely used in the pipeline as
        regular log message, but it allows messages to be associated
        with specific labels (mainly for packages,
        e.g. processCcd.isr).  The ``LEVEL`` is an integer, and
        messages with trace levels **below** the level you set will be
        shown.  So, the higher you set it, the more trace messages
        you'll see.
        
    --debug
        Enable debugging output.
    
    --doraise    
        Raise an exception on error (else log a message and continue)?
        Often, you don't want an exception to bring down the whole
        process.  But if you do (e.g. if you're trying to debug the
        exception), use this to prevent the exception from being
        handled.
        
    --logdest LOGDEST    
        Specify a file where log messages will be copied (they'll
        still appear on the terminal).
        
    --show [{config,data,tasks,run} [{config,data,tasks,run} ...]]
         Display the specified information to stdout and quit (unless
         run is specified).  The most useful option here is ``--show
         config``.  This is used to print the entire set of config
         parameters to the terminal.  What's even more useful is to
         use a glob to request only specific ones.  E.g. to see only
         the things matching '*background*', you can use ``--show
         config=*background*``.  Also useful is ``--show tasks``,
         which will print the tasks to be used by the command you're
         running.
         
    -j PROCESSES, --processes PROCESSES    
         Number of processes to use.  This uses Python multiprocessing
         to spawn processes on the same node.
                            
    -t PROCESSTIMEOUT, --process-timeout PROCESSTIMEOUT
         Timeout for multiprocessing; maximum wall time (sec).
                            
    --clobber-output    
         Remove and re-create the output directory if it already
         exists (safe with -j, but not all other forms of parallel
         execution).
                            
    --clobber-config
         Every time the pipeline runs, it stores the values for all
         configuration parameters, and EUPS versions for all ``setup``
         packages.  These parameters and versions are checked every
         time you try to run the pipeline in a given rerun.  If you've
         changed something (which would make your data inhomogeneous),
         the pipeline will refuse to run.  For production data, that's
         exactly what you want, but for testing you often don't care.
         By specifying ``--clobber-config``, the pipeline will make a
         backup of your config and eups version info (files in <data
         repo>/config/ will be moved: <foo> --> <foo>~1), and will
         overwrite existing config files instead of checking them.

    --id [KEY=VALUE1[^VALUE2[^VALUE3...] [KEY=VALUE1[^VALUE2[^VALUE3...] ...]]
         The data ID you wish to run, e.g. ``--id visit=12345
         ccd=1,2``.  For more info, see :ref:`data ID <back_dataId>`.
