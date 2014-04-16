

====================
Running the Pipeline
====================

There are two scripts which are used for running the pipeline,
depending on what you're trying to do: ``reduceFrames.py``, and
``hscProcessCcd.py``.  ``hscProcessCcd.py`` will bias subtract, flat
field, and then perform object detection and measurement on specified
visits and CCDs.  ``reduceFrames.py`` will perform these steps only
full visits.  As always, full usage statements can be found with
``--help`` or ``-h``.


reduceFrames.py
---------------

Example 1
^^^^^^^^^

::
   
   $ reduceFrames.py /data/Subaru/HSC --rerun cosmos_test --queue default \
      --job cosmos --nodes 2 --procs 12 --time 2000000 \
      --id field=COSMOS filter=NB0921 dateObs=2014-02-02

* ``/data/Subaru/HSC``      Location of the data
* ``--rerun cosmos_test``   The rerun where all outputs will be written.
* ``--id``                  The details of the inputs to run.  In this case, COSMOS data, in the NB0921 narrow band filter, taken on Feb 2, 2014.
* ``--queue default``       Name of the PBS torque queue
* ``--job s82``             Name the PBS job will have while running (``qstat`` will show this name)
* ``--nodes 2``             Run on two nodes of the cluster
* ``--procs 12``            Run 12 processes on each node

  
hscProcessCcd.py
-------------
  
Example 1
^^^^^^^^^

Here, I'll put some specific measurement algorithms to run in a
temporary config file (``tmp.config``), and then run the command with
that config to overload the defaults.  I'll also overload a config
parameter on the command line to disable fringe correction.

::

   # specify my own measurement algorithms to run in a temporary config file (omitting cmodel, in this case)
   $ cat tmp.config 
   root.measurement.algorithms.names=['flux.psf', 'flags.pixel', 'focalplane', 'flux.aperture',
   'flux.naive', 'flux.gaussian', 'centroid.naive', 'flux.sinc', 'shape.sdss', 'jacobian',
   'flux.kron', 'correctfluxes', 'classification.extendedness', 'skycoord']
   root.measurement.slots.modelFlux='flux.gaussian'
   
   $ hscProcessCcd.py /data/Subaru/HSC --rerun test --id visit=1252 ccd=50 \
      --clobber-config -C tmp.config --config isr.doFringe=False



makeSkyMap.py
-------------

Example 1
^^^^^^^^^

::
   
   $ makeSkyMap.py suprimecam /data1a/Subaru/SUPA/rerun/price-actj0022m0036 \
       --output=/data1a/work/price/actj0022m0036/ -C skymap-actj0022m0036.py

run_mosaicTask.py
-----------------

Example 1
^^^^^^^^^

::
   
   $ run_mosaicTask.py suprimecam /data1a/work/price/actj0022m0036 \
      --mosaicid field=ACTJ0022M0036 filter=W-S-I+

      
hscOverlaps.py
--------------

Example 1
^^^^^^^^^

::
   
   $ hscOverlaps.py suprimecam /data1a/work/price/actj0022m0036 --coadd deep \
       --id field=ACTJ0022M0036 filter=W-S-I+


hscStack.py
-----------

Example 1
^^^^^^^^^

::

   $ hscStack.py suprimecam /data1a/Subaru/SUPA/rerun/price-actj0022m0036 \
       --output /data1a/work/price/actj0022m0036 \
       --id field=ACTJ0022M0036 filter=W-S-I+ --filter W-S-I+ --tract 0 --patch 4,4
