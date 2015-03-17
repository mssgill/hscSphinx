
==========
simpleTask
==========

.. _simpletask:

The following is the most basic script which can be written using the
CmdLineTask.  A few simple config parameters are specified and used in
the Task.  The Task's intended purpose is coded in the ``run()``
method.  (A slightly more advanced example is shown in :ref:`nestedTask.py <nestedtask>`).

The ``simpleTask.py`` can be run with the simpleTools code.  To run it
with the real HSC pipeline code, simple change the ``import``
statements to switch underscore ``_`` to dot ``.``::

     import lsst.pex.config       as pexConfig
     import lsst.pipe.base        as pipeBase


The script will use the built-in help if you run with ``-h``::

     $ ./simpleTask.py -h
     
To run the script as you would run a pipeline script, with data in
``/path/to/data``, and even-numbered visits 100 to 110 with 2 cores::

     $ ./simpleTask.py /path/to/data -j 2 --id visit=100..110:2

To change the config parameters on the command line::

     $ ./simpleTask.py /path/to/data -j 2 --id visit=100..110:2 --config x=2.71828
     
     
.. literalinclude:: simpleTools/simpleTask.py

