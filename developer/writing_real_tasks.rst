

==================
Writing Real Tasks
==================

The following descripts how to write ``CmdLineTasks`` in various
levels of difficulty.  These code examples use the real pipeline and
are intended to demonstrate the sorts of things you might actually
want to do.

Reasons you might want to consider writing a Task include things like:

* You want to take advantage of the built-in handling of DataIds and parallel processing
* You want to running the pipeline in a way that's significantly different from the default

.. toctree::
   :hidden:

   findTract

:ref:`findTract.py <findtract>`

    This is a short example which creates a CmdLineTask to look-up the tract for a given visit,CCD.

.. findTract
.. runAFew
.. runPostISRCCD
