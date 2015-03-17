

========================
Core Pipeline Components
========================

.. _coreComponents:

The basic component of pipeline processing is called a Task.  A Task
is intended to contain a specific step in processing, e.g. detection,
measurement, etc.  Any such Task may have a number of configuration
parameters, and these are definied in Task-specific Config classes.
Understanding the ``Config`` class code is quite difficult, but is not
really required if you wish to understand and use the pipeline.  In
order to write a ``Task`` which uses these components, the most
important component to understand is probably the ``CmdLineTask``.

Here we provide a short description of how these different components
work, and we show a few simple examples Tasks.  If you're interested
in how to write a Task, you may want to skip ahead to the :ref:`examples <simpleExamples>`.

.. warning:: Each component shown here has been simplified to focus on the most important class methods so users will gain an understanding, without being overwhelmed by details.  We always provide information about where to find the actual code, if you wish to see it.  The actual pipeline code is much more robust, but also more difficult to explain.  We hope the following overview provides sufficient detail to allow users to understand the main concepts.

Download tarball :download:`simpleTools.tar`

.. toctree::
   :maxdepth: 2

   task
   cmdLineTask
   config
   argumentParser


How to Run a CmdLineTask
------------------------

.. _runCmdLineTask:

When you write a CmdLineTask in your own module, you create a runnable
script which is usually only a few lines.  Here's an example
``yourScript.py`` which imports ``yourModule`` where you've written a
class called ``YourCmdLineTask`` (which presumably inherits from
``CmdLineTask``)::

    #!/usr/bin/env python
    import yourModule
    yourModule.YourCmdLineTask.parserAndRun()

Here are a few examples showing how you run this example, written with
the simpleTools code.  The real pipeline code offers many more command
line options, but the ones shown are the most important.  First, a
help statement::

    $ simpleTask.py -h
    usage: simpleTask.py input [options]
    
    positional arguments:
      ROOT                  path to input data repository
    
    optional arguments:
      -h, --help            show this help message and exit
      -c [NAME=VALUE [NAME=VALUE ...]], --config [NAME=VALUE [NAME=VALUE ...]]
                            config override(s), e.g. -c foo=newfoo bar.baz=3
      -j PROCESSES, --processes PROCESSES
                            Number of processes to use
      --id [KEY=VALUE1[^VALUE2...] [KEY=VALUE1[^VALUE2...] ...]]
                            id parameters

``ROOT`` is the base of the directory tree where your data repository
lives.  The ``-c`` options is provided to allow you to override config
parameters by name on the command line.  ``--id`` is used to specify
which data you plan to run.  It should be followed by visits and CCDs
to run.  ``A..B:C`` is used to specify a range from A to B in
increments of C, and ``^`` is used to separate sequences.  ``-j N``
indicates the number of cores used to process the job in parallel.
Each entry from ``--id`` will be processed independently.  This
example shows processing data in ``/path/to/data``, and will look for
visits 100, 102, and 104, and CCDs 40 and 60.  These will be processed
in parallel with 2 cores::

     $ simpleTask.py /path/to/data --id visit=100..104:2 ccd=40^60 -j 2

In this case, the ``simpleTask.py`` example (see below) won't actually
look for any data; it will just loop through the values you've entered
and print them to stdout.

   
Simple CmdLineTask Examples
---------------------------

.. _simpleExamples:

The following are short examples intended to demonstrate how to write
``CmdLineTask`` scripts from scratch.  These Tasks don't attempt to
mimic the photometric pipeline, they just perform simple arithmetic
and print their output as a demonstration.  The ``simpleTask.py``
script contains a minimal example which prints a list of numbers.  The
``nestedTask.py`` script demonstrates a ``CmdLineTask`` which itself
contains and runs other ``Tasks``, each with separate ``Config``.

These are included with the :download:`simpleTools.tar` tarball.


.. toctree::
   :maxdepth: 2
   
   simpleTask
   nestedTask
