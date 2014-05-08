

=======================
Single Frame Processing
=======================

There are two scripts which are used for running the pipeline on
single-frame inputs, depending on what you're trying to do:
``reduceFrames.py``, and ``hscProcessCcd.py``.  ``hscProcessCcd.py``
will bias subtract, flat field, and then perform object detection and
measurement on specified visits and CCDs.  ``reduceFrames.py`` will
perform these steps only full visits.  All scripts will require a
:ref:`dataId <back_dataId>` of the form ``--id <identifiers>``, where
the identifiers are such things as ``visit``, ``ccd``, ``field``,
``dateObs``, ``filter``, etc.

As always, full usage statements can be found with ``--help`` or ``-h``


reduceFrames.py
---------------

As ``reduceFrames.py`` uses TORQUE, many of the command line arguments
are related to the batch processing, and are only briefly summarized.
For full details see :ref:`TORQUE <back_torque>`

**Example 1**

::
   
   $ reduceFrames.py /data/Subaru/HSC --rerun cosmos_test --queue small \
      --job cosmos --nodes 2 --procs 12 \
      --id field=COSMOS filter=HSC-I dateObs=2016-02-02

* ``/data/Subaru/HSC``      Location of the data
* ``--rerun cosmos_test``   The rerun where all outputs will be written.
* ``--id``                  Your dataId.  In this case, COSMOS data, in the HSC-I filter, taken Feb 2, 2016.
* ``--queue default``       Name of the PBS torque queue
* ``--job cosmos``          Name the PBS job will have while running (``qstat`` will show this name)
* ``--nodes 2``             Run on 2 nodes of the cluster
* ``--procs 12``            Run 12 processes on each node

  
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
   $ hscProcessCcd.py /data/Subaru/HSC --rerun test --id visit=1252 ccd=50 \
      --clobber-config -C tmp.config --config isr.doFringe=False


mosaic.py
^^^^^^^^^

Once the single-frame processing is completed, you can perform an
'ubercal' with mosaic.py.  This will solve for an improved astrometric
and photometric solution for a collection of visits.

**Example 1**

::
   
    $ mosaic.py /data/Subaru/HSC/rerun/mydata --mosaicid field=MYDATA filter=HSC-I

      
