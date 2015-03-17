
===========
CmdLineTask
===========

The ``CmdLineTask`` and ``TaskRunner`` are probably the most important
components to understand if you wish to see how the pipeline scripts
are executed.  The ``CmdLineTask`` inherits from a ``Task``, but
contains additional code to allow it to be used in executable scripts.
A ``CmdLineTask`` includes a pipeline ``ArgumentParser`` and a
``TaskRunner``, and can be used to quickly construct a runnable script
which can be run in the same way as pipeline scripts.

TaskRunner
----------

The ``TaskRunner`` is a class which separates the DataIds provided on
the command line and distributes them to be run in separate threads
with Python's ``multiprocessing`` module.


CmdLineTask
-----------

The ``CmdLineTask`` is a special class derived from a ``Task``.  By
encapsulating your code in the ``run()`` method of class derived from
a ``CmdLineTask``, you can easily create an executable script by
calling the ``parseAndRun()`` method on ``YourCmdLineTask``::

    #!/usr/bin/env python
    import yourModule
    yourModule.YourCmdLineTask.parserAndRun()
    

cmdLineTask.py
--------------
    
.. literalinclude:: simpleTools/lsst_pipe_base/cmdLineTask.py

