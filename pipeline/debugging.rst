

.. _debugging:

===============
Debugging Hints
===============

If for some reason you have trouble with any of the pipeline commands,
here are a few details which may help diagnose the problem.  If you've
found a specific problem and you have an error message, please check the
:ref:`Error Messages <errormessages>` section.


#. A TORQUE job will write its ``stdout`` to files with the form:
   jobname.nodename.NNNNN.  Jobname is what you call the submitted job
   by setting the ``--job foo`` command line argument.  Nodename is the
   node which sent its output to the file (probably called
   ``analysisNN``, NN is a number from 01 to 40), and NNNNN a number
   assigned by the scheduler.  If you suspect something went wrong
   with your job, have a look through a few of these files and see
   what the log messages say.

#. If the info in the TORQUE output files isn't helpful, you can try
   running the job in the current shell with the ``--do-exec`` option.
   HOWEVER, these jobs can be really big, so you should first try to
   reproduce the problem with a smaller subset of your data.  You can
   specify a few specific visits using ``..``, ``:`` and ``^`` to denote
   number ranges, e.g. ``--id visit=1234..1244:2 ccd=50`` (visits 1234
   to 1244 incrementing by 2, CCD 50 only) or ``--id visit=1234^1244
   ccd=40..60`` (visits 1234 and 1244, CCDs 40 to 60).

