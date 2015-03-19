
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
these catalogs are fine.  However, a blended object which is observed
in different bands, will not in general be deblended by the pipeline
in the same way in both e.g. HSC-I and HSC-R.  This means that R-I
colors based on ``stack.py`` catalogs are not consistent.  In order to
solve this, a final processing step has been added to compile a
catalog of sources detected in all bands, and ensure that the same
pixel footprints and deblending parameters are used for measurements
in all bands.

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
of course be set to make use of the available cluster resources.  This
single patch (3 filters) ran in approximately 2 hours on one core
at IPMU.

::

    $ multiBand.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 filter=HSC-R^HSC-I^HSC-Z --nodes 1 --procs 1 --mpiexec='-bind-to socket' --time 1000 --job multiband


Here, ``--job`` is simple the name of the job used by the PBS cluster,
and the ``--mpiexec='bind-to socket'`` option helps performance on the
PBS system.

    
Multiband Processing in Steps
-----------------------------

If you wish to run the multiband processing in separate steps, each
command is shown below with a description of what it does (the names
are quite self-explanatory), and with benchmark timings for how long
it took to run on a single core for this example.

    
detectCoaddSources.py
^^^^^^^^^^^^^^^^^^^^^

Detect sources and model background for the single band data (< 1 min)::

    $ detectCoaddSources.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 filter=HSC-R^HSC-I^HSC-Z


mergeCoaddDetections.py
^^^^^^^^^^^^^^^^^^^^^^^

Merge Footprints and Peaks from all detection images into a single, consistent set (< 1 min)::

    $ mergeCoaddDetections.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 filter=HSC-R^HSC-I^HSC-Z



measureCoaddSources.py
^^^^^^^^^^^^^^^^^^^^^^

Deblend and measure on per-band coadds (each band separately),
starting from consistent Footprints and Peaks (~ 60 min)::

    $ measureCoaddSources.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 filter=HSC-R^HSC-I^HSC-Z



mergeCoaddMeasurements.py
^^^^^^^^^^^^^^^^^^^^^^^^^

Merge the results from measurement from per-band coadds (~2 min).
This step essentially just chooses which band's measurement should be
used as a reference for the final measurement (the 'forced'
measurement ... see below)::

    $  mergeCoaddMeasurements.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 filter=HSC-R^HSC-I^HSC-Z



forcedPhotCoadd.py
^^^^^^^^^^^^^^^^^^

Perform forced measurements on per-band coadds.  This final step is
very similar to ``measureCoaddSources.py``, but now uses the fixed
parameters for the centroids and galaxy model ellipses *from the
reference band* chosen in ``mergeCoaddMeasurements.py`` (~35 min).::

    $ forcedPhotCoadd.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 filter=HSC-R^HSC-I^HSC-Z

