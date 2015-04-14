
.. _coadd_proc:

================
Coadd Processing
================

At this point, it is assumed that you've run reduceFrames.py to
complete the single-frame photometry.  If you haven't, go and do that
first.  Coadd construction is the process of warping exposures to put
them on a common WCS, and then combining them to produce a final
exposure with improved signal-to-noise ratio.  The process is
performed in a sequence of steps:

#. Make a **SkyMap** (the coordinate system used for coadd images)

#. **mosaic**: Performs an Uber-calibration

#. **Warp**: Resample the images from the observed WCS to the SkyMap coordinates.

#. **Assemble the coadd**: Statistically combine the warped images.

#. **Process** the coadd images (detect, measure, etc) to produce a catalog.


Each step is described below.  However, ``warp``, ``assemble``, and
``process`` can be run in a single script called ``stack.py`` (also
described below).


.. _skymap:

Making a SkyMap
---------------

Before stacking, you need to make a SkyMap.  A SkyMap is a tiling or
'tesselation' of the celestial sphere, and is used as coordinate
system for the final coadded image.  The largest region in the system
is called a 'Tract', and it contains smaller 'Patch' regions.  Both
tracts and patches overlap their neighbours.  By default, tracts
overlap by 1 arcmin, and patches overlap by 100 pixels (in a 4000x4000
patch).  Each tract contains a different WCS, but the WCSs used for
the patches within a given tract are just offset versions of the same
WCS.  In a later step, your input images will be warped from their
observed WCSs to the common WCS of the SkyMap.

There are two ways to create SkyMaps: (1) for the whole sky [probably
**not** what you want for individual PI-type observations], or (2) for
a selected region containing a set of exposures.


Full SkyMap
^^^^^^^^^^^

To create a full SkyMap (again, not likely what you want), do the following::
   
    $ makeSkyMap.py /data/Subaru/HSC/ --rerun=cosmos

If you're using a full SkyMap, the Tracts are a fixed system and you
may find you have to look-up which tracts your data live in.  If you
wish to look up a tract,patch for a specific visit,CCD, the
``hscOverlaps.py`` command can do this::

    $ hscOverlaps.py /data/Subaru/HSC --rerun=cosmos --id visit=1226 ccd=49 --coadd deep

There is also a Task example which can be used, see :ref:`findTract.py
<findTract>`.

Partial SkyMap
^^^^^^^^^^^^^^

To create a local SkyMap for the region containing your data, use the
``makeDiscreteSkyMap.py``.  Here, you can select specified visits to
be used to define the region of the SkyMap.  In this case the example
shows visits 1000 to 1020 with increment 2 (i.e. every other one, as
is the standard for HSC visit naming).  Because you chose a local
SkyMap, all your data will be within a single Tract, and that Tract
will be defined to have ID 0 (zero).

**(probably what you want)**

::

    $ makeDiscreteSkyMap.py /data/Subaru/HSC/ --rerun=cosmos --id visit=1000..1020:2


One of the example scripts (:ref:`showVisitSkyMap.py
<showvisitskymap>`) can be used to display a set of visits on a
SkyMap.  Here it was used to display two visits superimposed on a
discrete (partial) SkyMap.  Only the patches overlapped by the visits
are shown.  Each patch is labeled.

.. image:: ../images/showVisitSkyMap.png


Making a Custom SkyMap
^^^^^^^^^^^^^^^^^^^^^^

If you have a particular need for your coadds to have a specific WCS,
you can also customize the SkyMap to have a given pixel scale and
tangent point.  This is done by specifying config parameters to
``makeSkyMap.py`` as follows::

    $ cat overrides.config
    root.skyMap = "discrete"
    root.skyMap["discrete"].raList = [149.9]
    root.skyMap["discrete"].decList = [2.3]
    root.skyMap["discrete"].radiusList = [0.35]
    root.skyMap["discrete"].pixelScale = 0.2
    root.skyMap["discrete"].projection = "TAN"
    root.skyMap["discrete"].tractOverlap = 0

    $ makeSkyMap.py /data/Subaru/HSC --rerun=cosmos --configfile overrides.config


Large Discrete SkyMaps
^^^^^^^^^^^^^^^^^^^^^^

When a discrete SkyMap becomes large, various problems may occur.  The
projection used is a tangent projection and it may not be suitable
near the edges if your tract is very large.  Another (more rigid)
issue is that the **patch number must be less than 32** (i.e. the
largest discrete SkyMap is 32x32 patches).  If you really must use a
discrete SkyMap and your area is too large to fit in 32x32 patches,
you have two options:

* Adjust the patchInnerDimensions config parameter to use larger
  patches (the default is 4000,4000)::

    root.skyMap["discrete"].patchInnerDimensions = (5000,5000)

* Use multiple tracts in a discrete SkyMap.  Each 'list'-type
  parameter will allow multiple values to be specified, and tract
  numbers will be assigned in order.  Thus, the following override
  file would produce a skymap with two adjacent tracts centered on
  RA/Dec 149.7/2.3 and 150.1/2.3, which would be referred to as tracts
  0 and 1::

    $ cat overrides.config
    root.skyMap = "discrete"
    root.skyMap["discrete"].raList = [149.7,150.1]
    root.skyMap["discrete"].decList = [2.3, 2.3]
    root.skyMap["discrete"].radiusList = [0.35, 0.35]
    root.skyMap["discrete"].pixelScale = 0.2
    root.skyMap["discrete"].projection = "TAN"
    root.skyMap["discrete"].tractOverlap = 0


.. _mosaic:

mosaic.py
^^^^^^^^^

Once the single-frame processing is completed and you have a SkyMap,
you can perform an 'ubercal' with mosaic.py.  This will solve for an
improved astrometric and photometric solution for a collection of
visits.  In the ``--id``, you must specify the tract in addition to
the identifiers for your data (i.e. visit, field, filter, etc.).  If
you constructed a partial SkyMap, the tract will be 0.  It's also
useful to specify ccd=0..103.  CCDs 104 to 111 exist but are not used
for science data (4 auto-guide plus 8 auto-focus), and should not be
included.

::
   
    $ mosaic.py /data/Subaru/HSC/ --rerun=cosmos --id tract=0 visit=1000..1020:2 ccd=0..103


Depending on the number of input visits, the mosaic solution can take
some time to complete.  It can't currently make use of parallelization
on a cluster.

    
.. _stack:    

Coadd Processing with One Command
---------------------------------

If you just want to produce a coadd and run the pipeline on the
coadded image, then ``stack.py`` is the command you should use::

    $ stack.py /data/Subaru/HSC/ --rerun=cosmos --id tract=0 filter=HSC-I --selectId visit=1000..1020:2 --queue small --nodes 4 --procs 6 --job stack
    

In the example, the input visits are specified with ``--selectId``
(even-numbered visits from 1000 to 1020).  The ``--id`` parameter is
now used to specify the tract and patch dataId for the output.  If you
constructed a partial SkyMap with ``makeDiscreteSkyMap.py``, then your
tract number will be 0.  ``stack.py`` distributes jobs over a batch
processing system (PBS TORQUE or Slurm), and the remaining command
line arguments shown are related the batch processing.  See
:ref:`Batch Processing <back_batch>` for details.

.. _coadd_rerun_change:

Writing Coadd outputs to a different Rerun
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coadd processing involves loading input data which are themselves
outputs of an earlier pipeline stage.  In the example above, the coadd
outputs will be written to the same rerun from which the inputs were
loaded.  However, it's not unusual to want to write the coadd outputs
to a different location.  There are a few ways to do that.

* Use a colon to separate in_rerun from out_rerun ``--rerun=in_rerun:out_rerun``, e.g. ::

    $ stack.py /data/Subaru/HSC --rerun=cosmos:cosmos_coadd --id tract=0 filter=HSC-I --selectId visit=1000..1020:2 --queue small --nodes 4 --procs 6 --job stack

This will produce a new rerun directory called ``cosmos_coadd`` in the
main ``/data/Subaru/HSC/rerun`` directory.
    
* Use ``/data/Subaru/HSC/rerun/in_rerun --rerun=out_rerun``, e.g.::

    $ stack.py /data/Subaru/HSC/rerun/cosmos --rerun=cosmos_coadd --id tract=0 filter=HSC-I --selectId visit=1000..1020:2 --queue small --nodes 4 --procs 6 --job stack

This will produce a new rerun directory tree ``rerun/cosmos_coadd``
**which is a subdirectory** in the input ``cosmos`` rerun, i.e.:
``/data/Subaru/HSC/rerun/cosmos/rerun/cosmos_coass`` directory.

    
* Use ``--output=/totally/different/path/out_rerun``, e.g.::

    $ stack.py /data/Subaru/HSC/rerun/cosmos --output=/data/work/cosmos_coadd --id tract=0 filter=HSC-I --selectId visit=1000..1020:2 --queue small --nodes 4 --procs 6 --job stack

This will write all outputs to a new directory
``/data/work/cosmos_coadd``.  This option does not require that the
output rerun be located in the main data repository.

Restacking
^^^^^^^^^^

If you've completed the single-frame processing and wish to build and
process coadds multiple times (for debugging, or to test the effects
of different input parameters), you will need to write to different
output reruns (see :ref:`coadd_rerun_change`).  If coadds have already
been produced in a rerun directory, you'll want to specify a separate
``--output`` location or use ``--rerun=inrerun:outrerun``, and you
will also need to ``--clobber-config``, and enable output overwrites
with ``--config doOverwriteOutput=True doOverwriteCoadd=True
makeCoaddTempExp.doOverwrite=True`` (yes, even though outputs will be
written to a new location, you must still enable overwriting)::

    $ stack.py /data/Subaru/HSC/rerun/cosmos --output=/data/work/cosmos_coadd --id tract=0 filter=HSC-I --selectId visit=1000..1020:2 --queue small --nodes 4 --procs 6 --job stack --clobber-config --config doOverwriteOutput=True doOverwriteCoadd=True makeCoaddTempExp.doOverwrite=True

 

Coadd Processing in Steps
-------------------------

If you wish to do your coadd processing in individual steps, you can
forego ``stack.py``, and perform each of its component steps manually.

First, you must resample your single-frame output images to the
coordinate system used for coadds (the SkyMap you just created).  The
process is called 'warping', and will convert your input CCDs to
'patches'.  The corners of a given CCD will almost always lie across
patch borders, as CCDs and patches don't (can't) align perfectly.
Thus, each CCD will contribute to 4 patches.  The part of each patch
which is outside the region of the input CCD contains no data and is
masked in the 'warped' image.

In the second step, the warped images are combined statistically
with ``assembleCoadd.py`` to produce the 'coadd' or 'stack'.

The final part of coadd processing is to run detection and measurement
with ``hscProcessCoadd.py``.

.. _warp:
          
Warping
^^^^^^^
       
The first step is to warp your images to the SkyMap coordinate system
(Tracts and Patches).  This is done with makeCoaddTempExp.py::

    $ makeCoaddTempExp.py /data/Subaru/HSC --rerun cosmos --id tract=9000 patch=1,1 filter=HSC-Y --selectId visit=1000^1002 ccd=0..103

There are now two ``id`` settings required.  ``--id`` refers to the
Tract and Patch that you wish to create, while ``--selectId`` refers
to the *input* visits, CCDs, etc. that you wish warp to the specified
tract and patch.

.. _assemblecoadd:

Coadding
^^^^^^^^

Once your images have been warped on to the SkyMap patches, running
``assembleCoadd.py`` will create the stacked image.  Again, there are
two sets of ``id`` settings: ``--id`` (the destination Tract,Patch),
and ``--selectId`` (the input visits,CCDs).  These should probably be
set to be the same as the settings you used for
``makeCoaddTempExp.py``::

    $ assembleCoadd.py /data/Subaru/HSC --rerun cosmos --id tract=9000 patch=1,1 filter=HSC-Y --selectId visit=1000^1002 ccd=0..103

Note that ``stack.py`` includes a background subtraction (done as part
of detectCoaddSources) which assembleCoadd does not have, and it also
does "safe clipping", which assembleCoadd does not do.

.. todo::

    Add examples for how to override useful parameters for different
    types of stacks.

    
.. _processcoadd:
        
Coadd Processing (i.e. detection, measurement)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running the pipeline on coadded images cannot be done with
``hscProcessCcd.py`` or ``reduceFrames.py``.  Instead, a separate
process ``hscProcessCoadd.py`` is used.  This example will process the
same Tract,Patch which has been constructed above with
``assembleCoadd.py``::
    
    $ hscProcessCoadd.py /data/Subaru/HSC --rerun cosmos --id tract=9000 patch=1,1 filter=HSC-Y

