
.. _data_repo:

=====================
The Data Repository
=====================

The HSC pipeline requires that its data be handled in a very
particular way.  To complicate matters, the developers make no
promises about how the data model might change in the future.  This
summary give a short description of the structure of the data
repository, but please keep in mind that the layout shouldn't be
relied upon.  If, for example, you write a script which happens to
look for a file in the pipeline data repo, it's quite possible that
the file's location may change in later versions of the pipeline.  It
may even disappear entirely!  Feel free to poke around, but keep in
mind that the data repo is intended to be written-to and read-from
only by the pipeline tools.  If you're interested in loading some
outputs from a rerun, your best option is to use the pipeline's
:ref:`butler <tool_butler>`, a tool designed to work with the files in
the repo.


.. _data_format:

The Data Format
---------------

A single HSC exposure includes 112 2048x4176 (trimmed) pixel CCDs, 8 for focus
and 104 for data.

Raw file names
^^^^^^^^^^^^^^

Subaru uses a strict file naming convention for raw data called a
**FRAMEID**: 4 characters + 8 digits.  Each HSC CCD produces 1 FITS
file with name ``HSC<1 char series><8-digit code>.fits``
(i.e. <FRAMEID>.fits). The 1-character 'series' is currently 'A', but
will be incremented to 'B', 'C', etc in the future.  The 8-digit code
is:

* The final 2 digits encode the CCD number, but the codings ``00 - 99`` aren't sufficient for 112 devices.  The camera is divided into 'even' and 'odd' halves, with 56 devices in each (see the :ref:`HSC Layout <hsc_layout>`, or NOAJ's official `CCD positions figure <http://www.naoj.org/Observing/Instruments/HSC/CCDPosition_20140811.png>`_).

* Device numbers 49 and 50 are unused, so CCD numbers for 56 devices run from ``00`` to ``57``.  (The positions for 49 and 50 are actually occupied by auto-guider CCDs which use a different read-out and different naming convention.)

* The parity (even/odd) of the 3rd-last digit encodes which half of the camera the device occupies.

* The HSC exposure number ('visit' in LSST terminology) uses only the even numbers.

As an example, two sequential exposures
for visits 100 and 102 would have the following raw files::

     Visit 100 even:  HSCA00010000.fits - HSCA00010057.fits
     Visit 100 odd :  HSCA00010100.fits - HSCA00010157.fits
     
     Visit 102 even:  HSCA00010200.fits - HSCA00010257.fits
     Visit 102 odd :  HSCA00010300.fits - HSCA00010357.fits

When these raw files are ingested into a data repository (see below),
the new files (often symlinks) are named using the convention
``HSC-<7-digit visit>-<3-digit CCD>.fits``, which easier for users to
understand.  The raw files from the above example would then be
renamed to::

     Visit 100 even and odd:  HSC-0000100-000.fits - HSC-0000100-111.fits
     
     Visit 102 even and odd:  HSC-0000102-000.fits - HSC-0000102-111.fits
     
This convention has practical implications!  One user recently tried
to ``rm`` the raw FITS files for unwanted frames taken in cloudy conditions,
but was unaware of the odd/even naming and deleted exactly half of the
intended files.

Data Volume
^^^^^^^^^^^

Each raw pixel is stored as a 16 bit integer, and the raw data for 1
CCD (including FITS header) is about 18 MB.  One full raw exposure is
about 2 GB.  The processed exposures' pixels are stored as 32-bit
float, but also include a 32-bit variance image, and a 16-bit flags
image, for a total of 80-bits/pixel.  Here are a few rules-of-thumb
for determining how much hard disk space you need to process your
data.

========================   ==================
Data                       Size
========================   ==================
1 raw CCD                  18 MB
1 raw exposure             2 GB  (112 CCDs)
1 processed CCD            82 MB
1 processed Exposure       11 GB (104 CCDs)
1 CCD's catalog            ~10MB - 30MB
1 exposure's catalogs      1-2 GB
**1 CCD (raw+proc+cat)**   **100 MB**
**1 exp (raw+proc+cat)**   **13 GB**
========================   ==================

Put another way, you can store **500 exposures/TB (raw), ~80 exposures
/ TB (processed)**.  Note that these estimates do not consider space
for coadds as such estimates depend entirely on the number of
exposures being stacked per pointing.


.. _ingest:

Creating a Data Repo and Ingesting Data
---------------------------------------

The pipeline code includes a program to take a collection of
``HSCA*.fits`` files and import (or rather 'ingest') them into a
pipeline-friendly directory tree.  To avoid doubling the disk space
used by your raw data, this ingest step can be done with symlinks.

To create an HSC data repo, and ingest your raw data into it (assuming
you already EUPS `setup` the pipeline)::

    # make the directory where you want the data repo to live
    $ mkdir /data/Subaru/HSC

    # add a '_mapper' file to tell the pipeline which camera the data came from
    $ echo lsst.obs.hsc.HscMapper > /data/Subaru/HSC/_mapper

    # ingest the HSCA*.fits files.  The first time you do this, use '--create'
    $ hscIngestImages.py /data/Subaru/HSC --create --mode=link /path/to/rawdata/HSCA*.fits

You'll now see a newly created data repository in /data/Subaru/HSC/.
In addtion to the `_mapper` file you just created, it also contains a
directory tree named according the OBJECT entry in the FITS header
(M87 here), the DATE-OBS, the pointing, and the filter name.  The FITS
symlink itself has a name slightly different from the original raw
data file.  The format is HSC-VVVVVVV-CCC.fits, where V is a seven
digit 'visit' number, and 'C' is a 3 digit CCD number.  Lastly,
there's a sqlite database called the 'registry'.


Here's what it looks like with a single files ingested::

    $ tree /data/Subaru/HSC
    /data/Subaru/HSC/
    |-- M87
    |   `-- 2015-12-21
    |       `-- 00999
    |           `-- HSC-I
    |               `-- HSC-0001000-055.fits -> /data/work/rawdata/HSCA09870000.fits
    |-- _mapper
    `-- registry.sqlite3


The ingest step does two things: (1) copy (or symlink) the files into
the repo, and (2) make an entry in the registry database.  If you have
files which are already in place, and you just want to make an entry
into the registry database, use ``--mode=skip``.  Here's an example
registering ``M31`` data which is already in place in the repo.  (a
real example where the 2013-03-21/ directory was a symlink to use data
stored in another data repo::

    # register data which is already in place
    $ hscIngestImages.py /data/Subaru/HSC/ --mode=skip /data/Subaru/HSC/M31/2013-03-21/00100/HSC-I/HSC-*fits

    
Parallel Ingest
^^^^^^^^^^^^^^^

If you have good I/O (i.e., fast disks with lots of spindles,
generally not true for NFS mounted drives) you can use
``hscIngestImagesParallel.py``.  This can actually be run with even
more processes than there are cores (because time is spent doing the
I/O).  Here's an example if usage::

    $ hscIngestImagesParallel.py /data/Subaru/HSC --mode=link --procs=25 /path/to/rawdata/HSCA*.fits



.. _registryinfo:

Registry Information
^^^^^^^^^^^^^^^^^^^^

The registry file contains one entry for every file ingested, and it
is possible to query it with the ``registryInfo.py`` command.  Many
stages of pipeline processing require you to use some combination of
visit numbers (i.e. frameID), fields, dates, etc. to specify the input
data, and ``registryInfo.py`` makes it straightforward to find out
various details about the ingested files::

    # get a listing of all COSMOS data taken in filter HSC-I
    $ registryInfo.py /data/Subaru/HSC/registry.sqlite3 --field COSMOS --filter HSC-I
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112
    ...
    
To avoid having to type the path to the registry file, you can specify
the data repository directory in the SUPRIME_DATA_DIR environment
variable::

    $ export SUPRIME_DATA_DIR=/data/Subaru/HSC

    # now registryInfo.py can find the registry.sqlite3 file on its own
    $ registryInfo.py --field COSMOS --filter HSC-I
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112
    ...
    
On systems where the ``suprime_data`` EUPS package exists, the
SUPRIME_DATA_DIR is best setup with ``setup suprime_data``.  The
manager of the system should have configured that package to point to
the most up-to-date data set.  If multiple versions of
``suprime_data`` are present (check ``eups list suprime_data``), the
version names should indicate which data they contain::

    $ setup suprime_data
    $ registryInfo.py --visit 1234
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112

    
The Structure of a Rerun Directory
----------------------------------

Eventually, you may need to snoop around looking for your output data.
Each processing batch is referred to as a rerun, and new reruns will
appear in a ``rerun`` directory within your data repository.  A full
processing run takes place in multiple stages, but can loosely be
lumped together as single-frame processing, and coadd processing.
There are different outputs associated with each.


The single-frame outputs
^^^^^^^^^^^^^^^^^^^^^^^^

Here's a short look at the structure of a single-frame rerun called
``test``.  In this example, for clarity only one HSC CCD was processed
(CCD 50 in visit 1236), but a full HSC rerun would contain 112 (104 on-sky + 8
focus) CCDs for each visit processed::

    /data/Subaru/HSC/rerun/test/    
    |-- 00100                                         The pointing
    |   `-- HSC-I                                     The filter
    
    |       |-- corr                                  Corrected frames
    |       |   |-- BKGD-0001236-050.fits             The background (not easily readable)
    |       |   `-- CORR-0001236-050.fits             The corrected image
    
    |       |-- output                                Output data (i.e. measurements)
    |       |   |-- ICSRC-0001236-050.fits                
    |       |   |-- MATCH-0001236-050.fits            Objects matched to catalog sources
    |       |   |-- ML-0001236-050.fits                   
    |       |   |-- SRC-0001236-050.fits              Measurements on sources
    |       |   |-- SRCMATCH-0001236-050.fits             
    |       |   `-- SRCML-0001236-050.fits
    
    |       |-- processCcd_metadata                   pipeline internals
    |       |   `-- 0001236-050.boost
    
    |       |-- qa                                    Quality Assurance data and figures
    |       |   |-- ellPaGrid-0001236-050.fits
    |       |   |-- ellipseGrid-0001236-050.png
    |       |   |-- ellipseMap-0001236-050.png
    |       |   |-- ellipticityGrid-0001236-050.fits
    |       |   |-- ellipticityGrid-0001236-050.png
    |       |   |-- ellipticityMap-0001236-050.png
    |       |   |-- fwhmGrid-0001236-050.fits
    |       |   |-- fwhmGrid-0001236-050.png
    |       |   |-- magHist-0001236-050.png
    |       |   |-- psfModelGrid-0001236-050.fits
    |       |   |-- psfModelGrid-0001236-050.png
    |       |   |-- psfSrcGrid-0001236-050.fits
    |       |   |-- psfSrcGrid-0001236-050.png
    |       |   |-- seeingGrid-0001236-050.txt
    |       |   |-- seeingMap-0001236-050.png
    |       |   |-- seeingMap-0001236-050.txt
    |       |   |-- seeingRobust-0001236-050.png
    |       |   `-- seeingRough-0001236-050.png
    |       `-- thumbs                                Thumbnail figures
    |           |-- flattened-0001236-050.png
    |           `-- oss-0001236-050.png
    
    |-- _parent -> /data/Subaru/HSC                   A link back to the root of the data repo
    
    |-- config                                        Parameters specific to this rerun
    |   |-- eups.versions                             Package versions (file~1 contains clobbered versions)
    |   `-- processCcd.py                             Configuration parameters (file~1 contains clobbered parameters)
    
    `-- schema
        |-- icSrc.fits
        `-- src.fits


The mosaic outputs
^^^^^^^^^^^^^^^^^^

After single-frame processing, a global astrometric and photometric
solution (also called an 'uber-calibration') is computed with
``mosaic.py`` (see :ref:`Mosaic <mosaic>`).  This process will add two
files for each CCD in each tract.  The files will appear in the
``corr/<TRACT>`` directory.  For the example above, assuming tract
'0000' (i.e. a discrete skymap) and visits 1236 and 1238 (mosaic only
makes sense with multiple visits)::

    /data/Subaru/HSC/rerun/test/
    `-- 00100                                         The pointing
        `-- HSC-I                                     The filter
            `-- corr
                `-- 0000
                    |-- fcr-0001236-050.fits          # photometric corrections for global solution
                    |-- fcr-0001238-050.fits
                    |-- wcs-0001236-050.fits          # astrometric corrections for global solution
                    `-- wcs-0001238-050.fits


The Coadd outputs
^^^^^^^^^^^^^^^^^

The coadd outputs are produced by ``stack.py`` (see :ref:`Coadd
Processing <coadd_proc>`).  They live in one of two directories in the
data repository: ``deepCoadd/`` and ``deepCoadd-results/``.  Below,
the structures of both of these are show.  Although the entire process
can be handled by ``stack.py``, each sub-processing step can be run
independently, so the relevant script is shown with each file.

This example shows the outputs for a run of ``stack.py`` to make a
single patch coadd for some of the HSC SSP data, specifically HSC-I
visits 1228 and 1238.  This dataset was specially chosen to show a
single patch (number 1,1), but in general there would be similar files
for all patchs (typically up to patch 10,10, but depending on how the
skymap is configured, you may have more patches per tract).

The first step in coadding is to create a skymap.  The skymap is then
used to warp the input images to a common coordinate system for the
final coadd.  Outputs for these steps are shown in the ``deepCoadd/``
directory.

::

    $ tree /data/Subaru/HSC/rerun/myrerun/deepCoadd/
    /data/Subaru/HSC/rerun/myrerun/deepCoadd/
    |-- HSC-I
    |   `-- 0
    |       |-- 1,1
    |       |   |-- warp-HSC-I-0-1,1-1228.fits        # visit 1228 warped to tract/patch = 0/1,1
    |       |   `-- warp-HSC-I-0-1,1-1238.fits        # visit 1238 warped to tract/patch = 0/1,1
    |       `-- 1,1.fits                              # coadd of all tract/patch = 0/1,1 warps
    `-- skyMap.pickle                                 # the skymap


Measurements on the coadd (``1,1.fits`` above) are stored in the
``deepCoadd-results/`` directory.  The main source catalog is in the
``src-HSC-I-0-1,1.fits`` file.
    
::

    $ tree /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    `-- HSC-I
        `-- 0
            `-- 1,1
                |-- src-HSC-I-0-1,1.fits              # measurements on sources in tract/patch 0/1,1
                |-- srcMatch-HSC-I-0-1,1.fits
                `-- srcMatchFull-HSC-I-0-1,1.fits




The Multiband outputs
^^^^^^^^^^^^^^^^^^^^^

Recall that the purpose of the ``multiBand.py`` script is to perform
consistent measurements on coadds in different filters.  For this
example, directories for both HSC-I and HSC-R are shown, but in
general you should expect to see a separate directory tree for each
filter you ran in ``multiBand.py``.

As with ``stack.py``, the steps in ``multiBand.py`` can be run
separately (see :ref:`Multiband Processing <multiband_proc>`).  When
each step is run independently, a few extra intermediate files are
written, so in this example *all* files are shown.  If you run
``multiBand.py``, the ``detectMD-*`` and ``measMD-`` files will not be
written by default, and that's been marked in the file list.

::

    $ tree /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    |-- HSC-I
    |   `-- 0
    |       `-- 1,1
    |           |-- bkgd-HSC-I-0-1,1.fits             # detectCoaddSources.py
    |           |-- det-HSC-I-0-1,1.fits              # detectCoaddSources.py
    |           |-- detectMD-HSC-I-0-1,1.boost        # detectCoaddSources.py      (not with multiBand.py)
    |           |-- forced_src-HSC-I-0-1,1.fits       # forcedPhotCoadd.py
    |           |-- meas-HSC-I-0-1,1.fits             # measureCoaddSources.py
    |           |-- measMD-HSC-I-0-1,1.boost          # measureCoaddSources.py     (not with multiBand.py)
    |           `-- srcMatch-HSC-I-0-1,1.fits         # measureCoaddSources.py
    |-- HSC-R
    |   `-- 0
    |       `-- 1,1
    |           |-- bkgd-HSC-R-0-1,1.fits             # detectCoaddSources.py
    |           |-- det-HSC-R-0-1,1.fits              # detectCoaddSources.py
    |           |-- detectMD-HSC-R-0-1,1.boost        # detectCoaddSources.py      (not with multiBand.py)
    |           |-- forced_src-HSC-R-0-1,1.fits       # forcedPhotCoadd.py
    |           |-- meas-HSC-R-0-1,1.fits             # measureCoaddSources.py
    |           |-- measMD-HSC-R-0-1,1.boost          # measureCoaddSources.py     (not with multiBand.py)
    |           `-- srcMatch-HSC-R-0-1,1.fits         # measureCoaddSources.py
    `-- merged
        `-- 0
            `-- 1,1
                |-- mergeDet-0-1,1.fits               # mergeCoaddDetections.py
                `-- ref-0-1,1.fits                    # mergeCoaddMeasurements.py


