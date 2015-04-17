

====
Task
====

The Task is the fundamental unit of processing used in the pipeline.
All major components of the pipeline are contained in classes which
inherit from a Task, with the main executable code typically in a
``run()`` method.  Below is a short summary of the Task used by the
pipeline.  It contains only the essential components, but it
demonstrates the functionality of the code.

task.py
-------

.. literalinclude:: simpleTools/lsst_pipe_base/task.py
