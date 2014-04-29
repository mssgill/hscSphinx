

====================
Running the Pipeline
====================

There are two scripts which are used for running the pipeline,
depending on what you're trying to do: ``reduceFrames.py``, and
``hscProcessCcd.py``.  ``hscProcessCcd.py`` will bias subtract, flat
field, and then perform object detection and measurement on specified
visits and CCDs.  ``reduceFrames.py`` will perform these steps only
full visits.  All scripts will an input identifier of the form ``--id
<identifiers>``, where the identifiers are such things as ``visit``,
``ccd``, ``field``, ``dateObs``, ``filter``, etc.  In the examples
here, a variety of specific values are shown, but you're pretty much
free to use whatever you deem appropriate for the data that you're
running.

As always, full usage statements can be found with ``--help`` or ``-h``



Single Frame Processing
-----------------------

reduceFrames.py
^^^^^^^^^^^^^^^

**Example 1**

::
   
   $ reduceFrames.py /data/Subaru/HSC --rerun cosmos_test --queue default \
      --job cosmos --nodes 2 --procs 12 --time 2000000 \
      --id field=COSMOS filter=NB0921 dateObs=2014-02-02

* ``/data/Subaru/HSC``      Location of the data
* ``--rerun cosmos_test``   The rerun where all outputs will be written.
* ``--id``                  The details of the inputs to run.  In this case, COSMOS data, in the NB0921 narrow band filter, taken on Feb 2, 2014.
* ``--queue default``       Name of the PBS torque queue
* ``--job cosmos``          Name the PBS job will have while running (``qstat`` will show this name)
* ``--nodes 2``             Run on two nodes of the cluster
* ``--procs 12``            Run 12 processes on each node

  
hscProcessCcd.py
^^^^^^^^^^^^^^^^
  
**Example 1**


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


mosaic.py
^^^^^^^^^

Once the single-frame processing is completed, you can perform an 'ubercal' with mosaic.py.  This will solve for an improved astrometric and photometric solution for a collection of visits.

**Example 1**

::
   
    $ mosaic.py /data/Subaru/HSC/rerun/mydata --mosaicid field=MYDATA filter=HSC-I

      

Building Coadds
---------------

Coadd construction is the process of warping exposures to put them on
a common WCS, and then combining them to produce a final exposure
having an improved signat-to-noise ratio.  The process is performed in
a sequence of steps, and each is described below.  At this point, it
is assumed that you've run reduceFrames.py to complete the
single-frame photometry.


SkyMap
^^^^^^

A SkyMap is a tiling or 'tesselation' of the celestial sphere, and is
used as coordinate system for the final coadded image.  The largest
region in the system is called a 'Tract', and it contains smaller
'Patch' regions. Your input images will be warped from their observed
WCS to the common WCS of the SkyMap.  To create a SkyMap, do the following:

**Example 1**

::
   
    $ makeSkyMap.py /data/Subaru/HSC/


Warping
^^^^^^^
       
The next step is to warp your images to the SkyMap coordinate system
(Tracts and Patches).  This is done with makeCoaddTempExp.py::

**Example 1**

::

    $ makeCoaddTempExp.py /data/Subaru/HSC --rerun mydata \
        --id tract=9000 patch=1,1 filter=HSC-Y \
        --selectId visit=1000^1002 ccd=0..103

Here, there are now two ``id`` settings required.  ``--id`` refers to
the Tract and Patch that you wish to create, while ``--selectId``
refers to the *input* visits, CCDs, etc. that you wish warp to the
specified tract and patch.


Coadding
^^^^^^^^

Once your images have been warped on to the SkyMap patches, running
``assembleCoadd.py`` will create the stacked image.  Again, there are
two sets of ``id`` settings: ``--id`` (the destination Tract,Patch),
and ``--selectId`` (the input visits,CCDs).  These should probably be
set to be the same as the settings you used for
``makeCoaddTempExp.py``::

    $ assembleCoadd.py /data/Subaru/HSC --rerun mydata \
        --id tract=9000 patch=1,1 filter=HSC-Y \
        --selectId visit=1000^1002 ccd=0..103

        
Coadd Processing (i.e. detection, measurement)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running the pipeline on coadded images cannot be done with
``hscProcessCcd.py`` or ``reduceFrames.py``.  Instead, a separate
process ``hscProcessCoadd.py`` is used.  This example will process the
same Tract,Patch which has been constructed above with
``assembleCoadd.py``::
    
    $ hscProcessCoadd.py /data/Subaru/HSC --rerun mydata \
        --id tract=9000 patch=1,1 filter=HSC-Y


    
.. todo::
    
   Is hscOverlaps.py still used?
   
.. todo::
   
   Is hscStack.py still used?

