
.. _multiband_proc:

====================
Multiband Processing
====================

The multiband processing is a post-processing step used to produce
consistent matched outputs for coadds in different filters.  If you're
interested in multiband photometry with coadds (almost all users are),
this step is essential.

The original planning for this processing was written up on the HSC
Wiki and is available to any HSC collaboration members who may be
interested in understanding the details: `Coadd Multiband Processing
<http://hscsurvey.pbworks.com/w/page/87953929/Coadd%20Multi-Band%20Processing>`_


Why you Can't Just Use outputs from stack.py
--------------------------------------------

The pipeline stacking script ``stack.py`` also produces source
catalogs for stacked coadds, and if you're only interested in one band
these catalogs are fine.  However, there are some obvious (and some
not-so-obvious) problems which occur when using these catalogs for
multiple filters.  Clearly, some objects will not have been detected
in all bands, and colors will not be available for those objects.
However, a more subtle problem occurs when measuring model magnitudes
on galaxies.

Forced Photometry
^^^^^^^^^^^^^^^^^

The problem of dealing with sources detected in only some bands is
handled with 'forced photometry'.  Forced photometry is a process in
which the coordinates from detections made in one image are used to
perform measurements in another image.  Typically, the detection image
is a specific filter, e.g. HSC-I, and the forced image was taken with
a different filter.  The purpose for this is to obtain fluxes for
objects which are too faint to be detected in a given filter.  For
example, if a source is detected in HSC-I but not in HSC-R, we can use
the coordinates measured in the HSC-I band image to 'force' measure a
flux in the HSC-R image.  By doing this, we can detect in e.g. HSC-I, and
still obtain G,R,I,Z,Y photometry for all sources, regardless of
whether or not they provided enough flux for detection (e.g. 5-sigma)
in any of the other bands.

Model magnitude issues
^^^^^^^^^^^^^^^^^^^^^^

To measure a galaxy flux in a consistent way, the same galaxy profile
parameters (exponential, de Vaucouleur) must be used in each filter
**[need ref]**.  The outputs of ``stack.py`` contain model magnitudes
based on different profile parameters, and colors based on these
measurements are not consistent.


The multiband solution
^^^^^^^^^^^^^^^^^^^^^^

In order to solve these issues, a final processing step has been added
to compile a catalog of sources detected in any of the observed bands,
and to ensure that the same pixel footprints, deblending parameters,
and model profiles are then used for measurements in all bands.

As with :ref:`coadd processing <coadd_proc>`, multiband processing can
be done with a single process ``multiBand.py``, or as a sequence of a
few steps.


Multiband Processing with One Command
-------------------------------------

If you just want multiband photometry and you don't care to deal with
the intermediate steps (i.e. most users), you should just run
``multiBand.py``.  The example provided below was used to process a
single tract/patch (0/1,1) for 3 bands: HSC-R, HSC-I and HSC-Z.  It
assumes that you've already run ``stack.py`` to produce the stacked
images in a rerun called 'myrerun'.  In this case, only a single patch
was processed to the parameters for the compute cluster (--nodes,
--procs) are set to 1.  For a real data processing run, these should
of course be set to make use of the available cluster resources.  For
reference, this single patch (3 filters) ran in approximately 2 hours
on one core at IPMU.  With 3 filters, we could have benefited from
distributing the job to 3 cores.

::

    $ multiBand.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z --nodes 1 --procs 1 --mpiexec='-bind-to socket' --time 1000 --job multiband


Here, ``--job`` is simply the name of the job used by the PBS cluster,
and the ``--mpiexec='bind-to socket'`` option helps performance on the
PBS system.


Writing Mulitband outputs to a different Rerun
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As with coadds, the multiband outputs can be written to a different
rerun than the one used for inputs.  See the section :ref:`Writing
Coadds to a different Rerun <coadd_rerun_change>` for details.

    
Multiband Processing in Steps
-----------------------------

If you wish to run the multiband processing in separate steps, each
command is shown below with a description of what it does (the names
are quite self-explanatory), and with benchmark timings for how long
it took to run on a single core for this example.

    
detectCoaddSources.py
^^^^^^^^^^^^^^^^^^^^^

.. note:: detectCoaddSources.py is scheduled to be run as a part of :ref:`stack.py <stack>`.  If you constructed your coadds with ``stack.py``, you may already have produced these outputs. 

Detect sources and model background for the single band data (< 1 min)::

    $ detectCoaddSources.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z


mergeCoaddDetections.py
^^^^^^^^^^^^^^^^^^^^^^^

Merge Footprints and Peaks from all detection images into a single, consistent set (< 1 min)::

    $ mergeCoaddDetections.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z



measureCoaddSources.py
^^^^^^^^^^^^^^^^^^^^^^

Deblend and measure on per-band coadds (each band separately),
starting from consistent Footprints and Peaks (~ 60 min)::

    $ measureCoaddSources.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z



mergeCoaddMeasurements.py
^^^^^^^^^^^^^^^^^^^^^^^^^

Merge the results from measurement from per-band coadds (~2 min).
This step essentially just chooses which band's measurement should be
used as a reference for the final measurement (the 'forced'
measurement ... see below)::

    $  mergeCoaddMeasurements.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z



forcedPhotCoadd.py
^^^^^^^^^^^^^^^^^^

Perform forced measurements on per-band coadds.  This final step is
very similar to ``measureCoaddSources.py``, but now uses the fixed
parameters for the centroids and galaxy model ellipses *from the
reference band* chosen in ``mergeCoaddMeasurements.py`` (~35 min).::

    $ forcedPhotCoadd.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z

