
==============
ArgumentParser
==============

The argument parser used by the pipeline is derived from the native
Python ``argparse`` ArgumentParser class.  A number of command line
arguments are needed for almost any pipeline task, so they are defined
here.  Any task which uses this argumentParser will automatically gain
all of the available command line arguments normally used in the
pipeline.  Among the most useful are special ``--id`` arguments which
allow HSC data to be specifically referenced.

The example below includes only the essential components of code in
argumentParser.py.  The original code is located in the ``pipe_base``
module.

argumentParser.py
-----------------

.. literalinclude:: simpleTools/lsst_pipe_base/argumentParser.py

