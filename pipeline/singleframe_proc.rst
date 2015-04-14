

=======================
Single Frame Processing
=======================

There are two scripts which are used for running the pipeline on
single-frame inputs, depending on what you're trying to do:
``reduceFrames.py``, and ``hscProcessCcd.py``.  ``hscProcessCcd.py``
will bias subtract, flat field, and then perform object detection and
measurement on specified visits and CCDs.  ``reduceFrames.py`` will
perform these steps only on full visits.  ``reduceFrames.py`` will also
perform a full astrometric solution for the exposure.  All scripts
will require a :ref:`dataId <back_dataId>` of the form ``--id
<identifiers>``, where the identifiers are such things as ``visit``,
``ccd``, ``field``, ``dateObs``, ``filter``, etc.

As always, full usage statements can be found with ``--help`` or ``-h``

.. _reduceframes:

reduceFrames.py
---------------

As ``reduceFrames.py`` uses TORQUE, many of the command line arguments
are related to the batch processing, and are only briefly summarized.
For full details see :ref:`Batch Processing <back_batch>`

**Example 1**

::
   
   $ reduceFrames.py /data/Subaru/HSC --rerun cosmos --queue small --job cosmos --nodes 2 --procs 12 --id field=COSMOS filter=HSC-I dateObs=2016-02-02

* ``/data/Subaru/HSC``      Location of the data
* ``--rerun cosmos``        The rerun where all outputs will be written.
* ``--id``                  Your dataId.  In this case, COSMOS data, in the HSC-I filter, taken Feb 2, 2016.
* ``--queue default``       Name of the batch queue
* ``--job cosmos``          Name the batch job will have while running (for PBS, ``qstat`` will show this name)
* ``--nodes 2``             Run on 2 nodes of the cluster
* ``--procs 12``            Run 12 processes on each node

.. _hscprocessccd:

hscProcessCcd.py
----------------
  
**Example 1**


Here, I'll put some specific measurement algorithms to run in a
temporary config file (``tmp.config``), and then run the command with
that config to overload the defaults.  I'll also overload a config
parameter on the command line to disable fringe correction.  These are
purely for the purpose of example, and shouldn't lead you to believe
that you should override these parameters in your run.

::

   # specify measurement algorithms to run in a temporary config file (omitting cmodel, in this case)
   
   $ cat tmp.config
   root.measurement.algorithms.names=['flux.psf', 'flags.pixel', 'focalplane', 'flux.aperture',
   'flux.naive', 'flux.gaussian', 'centroid.naive', 'flux.sinc', 'shape.sdss', 'jacobian',
   'flux.kron', 'correctfluxes', 'classification.extendedness', 'skycoord']
   root.measurement.slots.modelFlux='flux.gaussian'

   # specify the config file with -C, and pass in another override on the command line with --config
   $ hscProcessCcd.py /data/Subaru/HSC --rerun cosmos --id visit=1000 ccd=50 --clobber-config -C tmp.config --config isr.doFringe=False

   
* ``/data/Subaru/HSC``            Location of the data
* ``--rerun cosmos``              The rerun where all inputs are read, and outputs will be written.
* ``--id``                        Your dataId.  In this case, visit 1000, ccd 50.
* ``-C tmp.config``               Specify a file containing config parameters to override (shown above as tmp.config)
* ``--config isr.doFringe=False`` Pass in a config parameter on the command line. Here, this disables fringe correction, which is only necessary in HSC-Y.
* ``--clobber-config``            Needed if you've changed a config parameter since the last processing in this rerun.

.. warning::

    --clobber-config is only needed if you change a config parameter
      or an eups package which is setup while processing within a
      given rerun.  Once used, the data should be assumed to be
      inhomogeneous.

